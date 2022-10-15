from pydantic import Extra, BaseSettings


class Config(BaseSettings):
    superusers: list
    setu2_cd: int
    setu2_enable_groups: list
    proxies_socks5: str

    class Config:
        extra = Extra.ignore
        case_sensitive = False
