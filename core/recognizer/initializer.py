from core.config import AppConfig


class _Recognizer:
    def score(self, image: bytes) -> list:
        raise NotImplementedError("Use class from initRecognizer function")


def initRecognizer() -> _Recognizer:
    if AppConfig.ai.type == "DETECTRON2":
        import Det2Rec
        return Det2Rec.Det2Recognizer(
            AppConfig.ai.det2_cfgpath,
            AppConfig.ai.modelpath,
            AppConfig.ai.device,
            AppConfig.ai.classes
        )
    elif AppConfig.ai.type == "YOLO":
        import YoloRec
        return YoloRec.YoloRecognizer(
            AppConfig.ai.modelpath,
            AppConfig.ai.device,
            AppConfig.ai.classes
        )
    else:
        raise ValueError("Incorrect AI type specified")
