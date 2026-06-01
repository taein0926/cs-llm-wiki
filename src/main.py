import os
import subprocess
import tempfile
import json
from dataclasses import dataclass, field
from typing import Literal, Optional
from pathlib import Path

# --- 1. Gemini CLI Subprocess API Specification ---

OutputFormat = Literal["text", "json", "stream-json"]

@dataclass
class GeminiRequest:
    prompt: str
    cwd: Optional[str] = None
    output_format: OutputFormat = "text"
    session_id: Optional[str] = None
    resume: bool = False
    approval_mode: Optional[str] = "default"
    sandbox: bool = False
    policy: Optional[str] = None
    model: Optional[str] = None
    system_prompt: Optional[str] = None
    include_directories: list[str] = field(default_factory=list)
    raw_output: bool = False
    timeout_sec: int = 180  # Increased timeout for complex wiki generation

@dataclass
class GeminiResult:
    ok: bool
    returncode: int
    stdout: str
    stderr: str
    session_id: Optional[str] = None
    error: Optional[str] = None

def build_gemini_command(req: GeminiRequest) -> list[str]:
    exe = "gemini.cmd" if os.name == "nt" else "gemini"
    cmd = [exe]

    if req.session_id:
        cmd += ["--resume", str(req.session_id)]
    elif req.resume:
        cmd += ["--resume", "latest"]

    if req.approval_mode:
        cmd += ["--approval-mode", req.approval_mode]
    
    if req.sandbox:
        cmd.append("--sandbox")
    
    if req.policy:
        cmd += ["--policy", req.policy]

    if req.output_format != "text":
        cmd += ["-o", req.output_format]
    
    if req.raw_output:
        cmd.append("--raw-output")

    if req.model:
        cmd += ["-m", req.model]

    for d in req.include_directories:
        cmd += ["--include-directories", d]

    cmd += ["-p", req.prompt]

    return cmd

def run_gemini(req: GeminiRequest) -> GeminiResult:
    env = os.environ.copy()
    tmp_sys_path = None

    if req.system_prompt:
        # Create a temporary file for the system prompt as per API spec
        fd, tmp_sys_path = tempfile.mkstemp(suffix=".md", prefix="gemini_sys_")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(req.system_prompt)
            env["GEMINI_SYSTEM_MD"] = tmp_sys_path
            
            cmd = build_gemini_command(req)
            
            completed = subprocess.run(
                cmd,
                cwd=req.cwd,
                env=env,
                text=True,
                capture_output=True,
                timeout=req.timeout_sec,
                check=False,
                encoding="utf-8"
            )
            
            return GeminiResult(
                ok=completed.returncode == 0,
                returncode=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
                error=None if completed.returncode == 0 else f"Exit code {completed.returncode}",
            )
        except subprocess.TimeoutExpired as e:
            return GeminiResult(
                ok=False, returncode=-1,
                stdout=e.stdout.decode("utf-8") if e.stdout else "",
                stderr=e.stderr.decode("utf-8") if e.stderr else "",
                error=f"Timeout after {req.timeout_sec}s",
            )
        except Exception as e:
            return GeminiResult(
                ok=False, returncode=-1,
                stdout="", stderr="",
                error=str(e)
            )
        finally:
            if tmp_sys_path and os.path.exists(tmp_sys_path):
                os.unlink(tmp_sys_path)
    else:
        # Handle case without system prompt
        cmd = build_gemini_command(req)
        try:
            completed = subprocess.run(
                cmd,
                cwd=req.cwd,
                env=env,
                text=True,
                capture_output=True,
                timeout=req.timeout_sec,
                check=False,
                encoding="utf-8"
            )
            return GeminiResult(
                ok=completed.returncode == 0,
                returncode=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
            )
        except Exception as e:
            return GeminiResult(ok=False, returncode=-1, stdout="", stderr="", error=str(e))

# --- 2. Main Pipeline Logic ---

def main():
    # Paths configuration
    raw_dir = Path("data/raw")
    wiki_dir = Path("docs/wiki")
    config_dir = Path("config")
    scheme_dir = Path("docs/scheme")

    # Ensure wiki directory exists
    wiki_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load System Prompts and Templates
    try:
        agents_guideline = Path(config_dir / "AGENTS.md").read_text(encoding="utf-8")
        gemini_guideline = Path(config_dir / "GEMINI.md").read_text(encoding="utf-8")
        system_prompt = f"{agents_guideline}\n\n{gemini_guideline}"
        
        page_template = Path(scheme_dir / "page_template.md").read_text(encoding="utf-8")
    except FileNotFoundError as e:
        print(f"Error: Required configuration or scheme file missing: {e}")
        return

    # 2. Iterate through raw data
    if not raw_dir.exists():
        print(f"Error: Raw data directory '{raw_dir}' does not exist.")
        return

    raw_files = list(raw_dir.glob("*.txt"))
    if not raw_files:
        print("No .txt files found in data/raw/.")
        return

    print(f"Starting pipeline for {len(raw_files)} files...")

    for raw_file in raw_files:
        try:
            print(f"Processing: {raw_file.name}")
            raw_content = raw_file.read_text(encoding="utf-8")

            # 3. Construct Prompt
            main_prompt = f"""너는 제공된 시스템 지침을 따르는 위키 생성 Planner 에이전트야. 아래의 [Raw 데이터]를 분석하여 `docs/scheme/page_template.md` 스키마 양식에 완벽히 부합하는 마크다운 문서를 생성해줘. 
특히 본문 작성 시, 다른 주요 CS 개념(예: os_memory, net_sliding_window, net_arq 등)과 연관성이 있다면 위키 고유의 상호 참조 문맥이 형성되도록 마크다운 내부 링크 형식(예: [[net_sliding_window]])을 본문 내용에 자연스럽게 녹여내어 작성해라.

[참고 스키마 템플릿]:
{page_template}

[Raw 데이터]:
{raw_content}"""

            # 4. Request to Gemini CLI
            req = GeminiRequest(
                prompt=main_prompt,
                system_prompt=system_prompt,
                approval_mode="plan",
                output_format="text"
            )

            result = run_gemini(req)

            if result.ok:
                # 5. Save Output
                # Use the first part of the filename for the wiki page name (handle .txt.txt etc)
                wiki_filename = raw_file.name.split('.')[0] + ".md"
                output_path = wiki_dir / wiki_filename
                
                output_path.write_text(result.stdout, encoding="utf-8")
                print(f"Successfully created: {output_path}")
            else:
                print(f"Failed to process {raw_file.name}: {result.error}")
                if result.stderr:
                    print(f"Error Details: {result.stderr}")

        except Exception as e:
            print(f"An unexpected error occurred while processing {raw_file.name}: {e}")

if __name__ == "__main__":
    main()
