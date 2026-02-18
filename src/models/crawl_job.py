class CrawlJob:
    def __init__(self, job_id: int, total_count: int):
        self.job_id = job_id
        self.total_count = total_count
        self.success_count = 0
        self.failed_count = 0
        self.skipped_count = 0

    def increase_success(self):
        self.success_count += 1

    def increase_failed(self):
        self.failed_count += 1

    def increase_skipped(self):
        self.skipped_count += 1

    @property
    def percent(self):
        if self.total_count == 0:
            return 0
        return round((self.success_count / self.total_count) * 100, 2)