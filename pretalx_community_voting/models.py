from django.db import models


class Vote(models.Model):
    CHOICES = [
        ("NOT_INTERESTED", 0),
        ("SOMEWHAT_INTERESTED", 1),
        ("VERY_INTERESTED", 2),
    ]

    score = models.IntegerField(choices=CHOICES, default=0)
    submission = models.ForeignKey(
        to="submission.Submission",
        related_name="votes",
        on_delete=models.CASCADE,
    )
    # The hashed email addresses are always 16 bytes long => 32 characters
    user = models.CharField(max_length=32, blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Vote(score={self.score}, user={self.user}, timestamp={self.timestamp}, submission={self.submission.title})"
