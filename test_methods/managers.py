from django.db import models


class Sample_TestingManager(models.Manager):
    def create(self, test, sample):
        sample_test=self.create(testing=test, sample=sample)
        return sample_test