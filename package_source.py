"""Package an explicit source-file list. Private configuration is never included."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

FILES = [
    "app.py", "app_config.py", "study_engine.py", "chat_engine.py", "practice_settings.py",
    "styles.css",
    "check_live.py", "package_source.py", "requirements.txt", "start.ps1",
    "README.md", "LEARNING.md", "DEPLOY.md", "LICENSE", ".gitignore",
    "secrets.toml.example", ".streamlit/config.toml", "tests/test_study.py",
    ".21st/design.json", ".21st/DESIGN.md",
]


def main():
    root = Path(__file__).parent
    output = root / "dist" / "recall-source.zip"
    output.parent.mkdir(exist_ok=True)
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for name in FILES:
            archive.write(root / name, name)
    with ZipFile(output) as archive:
        assert ".streamlit/secrets.toml" not in archive.namelist()
        assert len(archive.namelist()) == len(FILES)
    print(f"Packaged {len(FILES)} source files. Private key and environment excluded.")


if __name__ == "__main__":
    main()
