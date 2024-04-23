from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Any

@dataclass(frozen=True)
class DataIngestionConfig:
    """
    Configuration for data ingestion process.
    
    Attributes:
    - root_dir: Directory where data ingestion artifacts are stored.
    - local_data_file: Path to the local file where the data is already saved.
    """
    root_dir: Path  # Directory where data ingestion artifacts are stored
    local_data_file: Path  # Path to the local file where the data is already saved


@dataclass(frozen=True)
class DataValidationConfig:
    """
    Configuration class for data validation.
    
    This class captures the essential configurations required for data validation, 
    including directories for storing validation results, paths to data files, 
    and the expected data schema.
    
    Attributes:
    -----------
    root_dir : Path
        Directory for storing validation results and related artifacts.
        
    data_source_file : Path
        Path to the ingested or feature-engineered data file.
        
    status_file : Path
        File for logging the validation status.
        
    schema : Dict[str, Dict[str, str]]
        Dictionary containing initial schema configurations for data validation.
    """
    
    root_dir: Path  # Directory for storing validation results and related artifacts
    data_source_file: Path  # Path to the ingested or feature-engineered data file
    status_file: Path  # File for logging the validation status
    schema: Dict[str, Dict[str, str]]  # Dictionary containing initial schema configurations

@dataclass(frozen=True)
class DataTransformationConfig:
    """
    Configuration for the data transformation process.
    
    This configuration class captures the necessary paths and directories 
    required for the transformation of data post-ingestion and pre-model training.
    
    Attributes:
    - root_dir: Directory where data transformation results and artifacts are stored.
    - data_source_file: Path to the file where the ingested data is stored that needs to be transformed.
    """
    
    root_dir: Path  # Directory for storing transformation results and related artifacts
    data_source_file: Path  # Path to the ingested data file for transformation
    data_validation: Path # Path to the validated output file
    normalization_dict: Path # Path to our abbreviation normalized dictionary


@dataclass
class SpacyNERConfig:
    """
    Represents the configuration for spaCy Named Entity Recognition (NER) model training.
    
    Attributes:
        root_dir (Path): Directory for storing training artifacts and results.
        ner_job_description_extractor_dir (Path): Directory containing the NER job description extractor model.
        json_annotated_path (Path): Path to the JSON file with annotations from Label Studio.
        output_path (Path): Destination path for the converted spaCy data format.
        train_data_path (Path): Path to the CSV file containing unannotated training data.
        test_data_path (Path): Path to the CSV file containing unannotated test data.
        val_data_path (Path): Path to the CSV file containing unannotated validation data.
        spacy_train (Path): Path for the processed spaCy training data.
        spacy_dev (Path): Path for the processed spaCy development (validation) data.
        original_dataset_path (Path): Path to the original dataset used for entity extraction.
        train_data_extracted_entities (Path): Path for the CSV file with entities extracted from the training data.
        merged_output_path (Path): Path for the merged dataset after combining original data with extracted entities.
        pretrained_model_dir (Path): Directory containing the pretrained model for fine-tuning.
        custom_model_dir (Path): Directory intended for storing the custom-trained model.
        gpu_allocator (str): The GPU allocator for training, e.g., 'pytorch'.
        components (List[Dict[str, Any]]): Configuration for the NER pipeline components.
        training (Dict[str, Any]): Dictionary containing the training parameters.
    """
    root_dir: Path
    ner_job_description_extractor_dir: Path
    json_annotated_path: Path
    output_path: Path
    train_data_path: Path
    test_data_path: Path
    val_data_path: Path
    spacy_train: Path
    spacy_dev: Path
    original_dataset_path: Path
    train_data_extracted_entities: Path
    merged_output_path: Path
    pretrained_model_dir: Path
    custom_model_dir: Path
    gpu_allocator: str
    components: List[Dict[str, Any]]
    training: Dict[str, Any]
    training_metrics_path_custom: Path
    training_metrics_path_finetuned: Path


@dataclass
class BERTopicConfig:
    root_dir: Path
    data_path: Path
    output_path: Path


@dataclass
class SemanticRoleLabelingConfig:
    root_dir: Path
    data_path: Path
    output_path: Path
    model_path: Path


@dataclass
class ContextualEmbedderConfig:
    # Path to the root directory where embedding artifacts will be stored.
    root_dir: Path
    
    # Path to the file containing results from Semantic Role Labeling (SRL) and possibly other analyses.
    results_path: Path
    
    # Path where the generated embeddings should be saved.
    output_path: Path
    
    # The name of the model to be used from SentenceTransformers for generating embeddings.
    model_name: str
