
from book_recommendation_system import logger
from book_recommendation_system.pipeline.stage_01_data_ingestion import (
    DataIngestionPipeline
)
from book_recommendation_system.pipeline.stage_02_data_validation import (
    DataValidationPipeline
)
from book_recommendation_system.pipeline.stage_03_data_transformation import (
    DataTransformationPipeline
)
from book_recommendation_system.pipeline.stage_04_model_trainer import (
    ModelTrainerPipeline
)

STAGE_NAME = "Data Ingestion"

try:
    logger.info(f">>>>> Stage {STAGE_NAME} started <<<<<<")
    data_ingestion = DataIngestionPipeline()
    data_ingestion.main()
    logger.info(f">>>>> Stage {STAGE_NAME} Completed <<<<<<")
except Exception as e:
    logger.exception(e)
    raise


STAGE_NAME = "Data Validation"

try:
    logger.info(f">>>>> Stage {STAGE_NAME} started <<<<<<")
    data_validation = DataValidationPipeline()
    data_validation.main()
    logger.info(f">>>>> Stage {STAGE_NAME} Completed <<<<<<")
except Exception as e:
    logger.exception(e)
    raise


STAGE_NAME = "Data Transformation"

try:
    logger.info(f">>>>> Stage {STAGE_NAME} started <<<<<<")
    data_transformation = DataTransformationPipeline()
    data_transformation.main()
    logger.info(f">>>>> Stage {STAGE_NAME} Completed <<<<<<")
except Exception as e:
    logger.exception(e)
    raise

STAGE_NAME = "Model Trainer"

try:
    logger.info(f">>>>> Stage {STAGE_NAME} started <<<<<<")
    model_trainer = ModelTrainerPipeline()
    model_trainer.main()
    logger.info(f">>>>> Stage {STAGE_NAME} Completed <<<<<<")
except Exception as e:
    logger.exception(e)
    raise