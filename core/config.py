import attrs

import environ


@environ.config(prefix="")
class Config:
    @environ.config
    class AI:
        @staticmethod
        def _str2list(s: str):
            return [] if not s else s.split(",")
        workers = environ.var(
            validator=attrs.validators.instance_of(int), converter=int)
        type = environ.var(validator=attrs.validators.instance_of(str))
        device = environ.var(validator=attrs.validators.instance_of(str))
        classes = environ.var(
            validator=attrs.validators.instance_of(list), converter=_str2list)
        modelpath = environ.var(validator=attrs.validators.instance_of(str))
        det2_cfgpath = environ.var(
            "",
            validator=attrs.validators.instance_of(str)
        )

    ai = environ.group(AI)
    HealthCheckTimeout = environ.var(
        validator=attrs.validators.instance_of(int), converter=int)
    Broker = environ.var(validator=attrs.validators.instance_of(str))
    FramesTopic = environ.var(validator=attrs.validators.instance_of(str))
    ConsumeGroup = environ.var(validator=attrs.validators.instance_of(str))
    DetectionsTopic = environ.var(validator=attrs.validators.instance_of(str))
    QueueLimit = environ.var(
        validator=attrs.validators.instance_of(int), converter=int)


AppConfig = environ.to_config(Config)
