#!/usr/bin/env python3
import argparse
import logging
from detector import DeepfakeDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Deepfake Detection System")

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--video", type=str)
    mode.add_argument("--image", type=str)
    mode.add_argument("--web", action="store_true")

    args = parser.parse_args()

    detector = DeepfakeDetector({
        "selected_model": "mesonet",
        "enable_ensemble": False,
        "use_gpu": True
    })

    if args.video:
        result = detector.analyze_video(args.video)
        print(result)

    elif args.image:
        result = detector.analyze_image(args.image)
        print(result)

    elif args.web:
        import subprocess
        subprocess.run(["streamlit", "run", "web_app.py"])

if __name__ == "__main__":
    main()
