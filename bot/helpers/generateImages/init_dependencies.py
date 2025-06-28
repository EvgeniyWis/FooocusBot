"""
This module initializes dependencies with circular imports to avoid import cycles.
"""

import logging

logger = logging.getLogger(__name__)


def init_dependencies():
    """
    Initialize all dependencies that have circular imports.
    This function should be called during application startup.
    """
    try:
        logger.info("Initializing dependencies with circular imports...")

        # Import locally to avoid circular imports during module loading
        # Set up the process_image_block in generateImageBlock
        import bot.helpers.generateImages.process_image_block as process_image_block_module
        from bot.helpers.generateImages.generateImageBlock import (
            set_process_image_block,
        )
        from bot.helpers.generateImages.process_image_block import (
            set_send_image_block,
        )

        set_process_image_block(process_image_block_module)

        # Set up sendImageBlock in process_image_block
        import bot.helpers.handlers.startGeneration.sendImageBlock as send_image_block_module

        set_send_image_block(send_image_block_module)

        logger.info(
            "Successfully initialized dependencies with circular imports"
        )

    except Exception as e:
        logger.error(f"Failed to initialize dependencies: {e}", exc_info=True)
        raise
