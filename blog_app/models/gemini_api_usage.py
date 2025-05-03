import logging

from django.db import models
from django.utils import timezone


class GeminiApiUsage(models.Model):
    """
    Model to track Gemini API usage metrics.
    """

    date = models.DateField(default=timezone.now)
    request_count = models.IntegerField(default=0)
    successful_requests = models.IntegerField(default=0)
    failed_requests = models.IntegerField(default=0)
    tokens_used = models.IntegerField(default=0)
    average_response_time = models.FloatField(default=0)
    model_name = models.CharField(max_length=100, default="gemini-2.5-pro-preview-03-25")
    last_error_message = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Gemini API Usage"
        verbose_name_plural = "Gemini API Usage"
        ordering = ["-date"]

    def __str__(self):
        return f"Gemini API Usage - {self.date}"

    @classmethod
    def log_request(cls, successful=True, tokens=0, response_time=0, model_name=None, error_message=None):
        """
        Log a Gemini API request.

        Args:
            successful (bool): Whether the request was successful
            tokens (int): Number of tokens used in the request
            response_time (float): Response time in seconds
            model_name (str): Name of the model used
            error_message (str): Error message if the request failed
        """
        logger = logging.getLogger("gemini_api_usage")
        today = timezone.now().date()

        # Get or create today's usage record
        usage, created = cls.objects.get_or_create(date=today)

        # Update metrics
        usage.request_count += 1
        if successful:
            usage.successful_requests += 1
        else:
            usage.failed_requests += 1
            usage.last_error_message = error_message

        # Update token usage
        usage.tokens_used += tokens

        # Update average response time
        if response_time > 0:
            if usage.average_response_time == 0:
                usage.average_response_time = response_time
            else:
                # Calculate new average
                total_requests = usage.successful_requests + usage.failed_requests
                usage.average_response_time = (
                    (usage.average_response_time * (total_requests - 1)) + response_time
                ) / total_requests

        # Update model name if provided
        if model_name:
            usage.model_name = model_name

        usage.save()

        logger.info(
            f"Gemini API request logged: success={successful}, tokens={tokens}, "
            f"response_time={response_time}, model={model_name or usage.model_name}"
        )

        return usage
