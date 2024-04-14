from src.career_chief.constants import *
from src.career_chief.utils.common import read_yaml, create_directories
from src.career_chief import logger
from src.career_chief.entity.config_entity import (DataIngestionConfig, 
                                                   DataValidationConfig, 
                                                   SpacyNERConfig,
                                                   BERTopicConfig)

import os

class ConfigurationManager:
    """
    ConfigurationManager manages configurations needed for the data pipeline.

    The class reads configuration, parameter, and schema settings from specified files
    and provides a set of methods to access these settings. It also takes care of
    creating necessary directories defined in the configurations.

    Attributes:
    - config (dict): Configuration settings.
    - params (dict): Parameters for the pipeline.
    - schema (dict): Schema information.
    """
    
    def __init__(self, 
                 config_filepath = CONFIG_FILE_PATH, 
                 params_filepath = PARAMS_FILE_PATH, 
                 schema_filepath = SCHEMA_FILE_PATH) -> None:
        """
        Initialize ConfigurationManager with configurations, parameters, and schema.

        Args:
        - config_filepath (Path): Path to the configuration file.
        - params_filepath (Path): Path to the parameters file.
        - schema_filepath (Path): Path to the schema file.

        Creates:
        - Directories specified in the configuration.
        """
        self.config = self._read_config_file(config_filepath, "config")
        self.params = self._read_config_file(params_filepath, "params")
        self.schema = self._read_config_file(schema_filepath, "initial_schema")

        # Create the directory for storing artifacts if it doesn't exist
        create_directories([self.config.artifacts_root])

    def _read_config_file(self, filepath: str, config_name: str) -> dict:
        """
        Read a configuration file and return its content.

        Args:
        - filepath (str): Path to the configuration file.
        - config_name (str): Name of the configuration (for logging purposes).

        Returns:
        - dict: Configuration settings.

        Raises:
        - Exception: If there's an error reading the file.
        """
        try:
            return read_yaml(filepath)
        except Exception as e:
            logger.error(f"Error reading {config_name} file: {filepath}. Error: {e}")
            raise

    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Extract and return data ingestion configurations as a DataIngestionConfig object.

        This method fetches settings related to data ingestion, like directories and file paths,
        and returns them as a DataIngestionConfig object.

        Returns:
        - DataIngestionConfig: Object containing data ingestion configuration settings.

        Raises:
        - AttributeError: If the 'data_ingestion' attribute does not exist in the config file.
        """
        try:
            config = self.config.data_ingestion
            # Create the root directory for data ingestion if it doesn't already exist
            create_directories([config.root_dir])
            
            return DataIngestionConfig(
                root_dir=Path(config.root_dir),
                local_data_file=Path(config.local_data_file),
            )

        except AttributeError as e:
            logger.error("The 'data_ingestion' attribute does not exist in the config file.")
            raise e
        
    
    def get_data_validation_config(self) -> DataValidationConfig:
        """
        Extracts data validation configurations and constructs a DataValidationConfig object.

        Returns:
        - DataValidationConfig: Object containing data validation configuration.

        Raises:
        - AttributeError: If the 'data_validation' attribute does not exist in the config.
        """
        try:
            # Extract data validation configurations
            config = self.config.data_validation
            
            # Extract schema for data validation
            
            schema = self.schema.columns
            logger.info(schema)
            
            # Ensure the directory for the status file exists
            create_directories([os.path.dirname(config.status_file)])

            # Construct and return the DataValidationConfig object
            return DataValidationConfig(
                root_dir=Path(config.root_dir),
                data_source_file=Path(config.data_source_file),
                status_file=Path(config.status_file),
                schema=schema
            )

        except AttributeError as e:
            # Log the error and re-raise the exception for handling by the caller
            logger.error("The 'data_validation' attribute does not exist in the config file.")
            raise e
        

    def get_spacy_ner_config(self) -> SpacyNERConfig:
        """
        Fetches and constructs the spaCy NER training configuration.

        Extracts settings related to spaCy NER model training from the loaded YAML
        configurations and returns them encapsulated in a SpacyNERConfig object.

        Returns:
        - SpacyNERConfig: Configuration object for spaCy NER model training.

        Raises:
        - KeyError: If any required configuration is missing.
        """
        try:
            ner_config = self.config['spacy_ner']
            
            return SpacyNERConfig(
                root_dir=Path(ner_config['root_dir']),
                ner_job_description_extractor_dir=Path(ner_config['ner_job_description_extractor_dir']),
                json_annotated_path=Path(ner_config['json_annotated_path']),
                output_path=Path(ner_config['output_path']),
                train_data_path=Path(ner_config['train_data_path']),
                test_data_path=Path(ner_config['test_data_path']),
                val_data_path=Path(ner_config['val_data_path']),
                spacy_train=Path(ner_config['spacy_train']),
                spacy_dev=Path(ner_config['spacy_dev']),
                original_dataset_path=Path(ner_config['original_dataset_path']),
                train_data_extracted_entities=Path(ner_config['train_data_extracted_entities']),
                merged_output_path=Path(ner_config['merged_output_path']),
                pretrained_model_dir=Path(ner_config['pretrained_model_dir']),
                custom_model_dir=Path(ner_config['custom_model_dir']),
                gpu_allocator=ner_config.get('gpu_allocator', False),
                components=ner_config.get('components', []),
                training=ner_config['training'],
                training_metrics_path_custom=ner_config['training_metrics_path_custom'],
                training_metrics_path_finetuned=ner_config['training_metrics_path_finetuned']
            )
        except KeyError as e:
            logger.error(f"A required configuration is missing in the 'spacy_ner' section: {e}")
            raise KeyError(f"Missing configuration in 'spacy_ner': {e}") from e
        
    
    def get_ber_topic_config(self) -> BERTopicConfig:
        
        try:
            ber_topic_config = self.config['ber_topic']
            
            return BERTopicConfig(
                root_dir=Path(ber_topic_config['root_dir']),
                data_path=Path(ber_topic_config['data_path']),
                output_path=Path(ber_topic_config['output_path']),
            )
        except KeyError as e:
            logger.error(f"A required configuration is missing in the 'ber_topic_config' section: {e}")
            raise KeyError(f"Missing configuration in 'ber_topic_config': {e}") from e