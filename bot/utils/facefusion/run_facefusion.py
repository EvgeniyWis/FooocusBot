import os
import subprocess


def run_facefusion(source_path: str, target_path: str, output_path: str):
    facefusion_path = os.path.abspath(
        "../../projects/facefusion/facefusion.py",
    )
    process = subprocess.run(
        [
            "python",
            facefusion_path,
            "headless-run",
            "--source",
            source_path,
            "--target",
            target_path,
            "--output-path",
            output_path,
            "--execution-providers",
            "cpu",
        ],
        capture_output=True,
        text=True,
    )

    return process.stdout, process.stderr


# TODO: можно удалять, если не нужно вручную протестировать
if __name__ == "__main__":
    source = "bot/images/faceswap/evanoir.xo.jpg"
    target = "bot/images/faceswap/face_nika_saintclair.jpg"
    output = "bot/images/faceswap/res.jpg"

    stdout, stderr = run_facefusion(source, target, output)

    print("STDOUT:\n", stdout)
    print("STDERR:\n", stderr)
