import ruamel.yaml
from typing import Any, Optional
import logging
from datetime import datetime, timezone
import os
import click
import decimal
import discord


class Logger():
    def __init__(self) -> None:
        self.logger = logging.getLogger()

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def warn(self, msg: str) -> None:
        self.logger.warn(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)
        exit(1)


class Configuration:
    logger: Optional[Logger] = None
    config_filepath: Optional[str] = None
    raw_config: Optional[Any] = None

    _binance_api_key: Optional[str] = None
    _binance_api_secret: Optional[str] = None

    def __init__(self, config_filename: str = 'config.yaml') -> None:
        config_dir = click.get_app_dir('css')
        self.logger = Logger()
        self.config_filepath = os.path.join(config_dir, config_filename)

        if not os.path.exists(self.config_filepath):
            self.logger.error('Config file {} not found.'.format(self.config_filepath))

        self.raw_config = parse_yaml_file(self.config_filepath)


def parse_yaml_file(filepath: str) -> Any:
    with open(filepath, 'r') as f:
        return ruamel.yaml.safe_load(f)  # type: ignore


def discord_send_message(message: str) -> None:
    cfg = Configuration()
    assert cfg is not None
    assert cfg.raw_config is not None
    assert cfg.logger is not None
    url = cfg.raw_config['discord_url']
    try:
        webhook = discord.Webhook.from_url(url, adapter=discord.RequestsWebhookAdapter())
        webhook.send(message)
    except Exception as e:
        cfg.logger.warn('Failed to send discord message: {}'.format(e))