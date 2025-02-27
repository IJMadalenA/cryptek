import logging

from transformers import pipeline

# Suppress the logging output from the transformers library
logging.getLogger("transformers").setLevel(logging.ERROR)


class CommentModeration:
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        self.moderation_pipeline = pipeline("sentiment-analysis", model=model_name)

    def moderate_comment(self, content: str, score_threshold: int = None) -> (bool, float):
        """
        Check if the comment content is acceptable.
        This method only admits a single comment as input.
        """
        if not isinstance(content, str):
            raise ValueError("The content must be a single string.")

        result = self.moderation_pipeline(content)[0]

        # Assuming that a positive sentiment means the comment is acceptable
        if score_threshold is None:
            return result["label"] == "POSITIVE", result["score"]
        else:
            return result["score"] > score_threshold, result["score"]
