from spidermon import Monitor, MonitorSuite, monitors
from spidermon.contrib.actions.email.ses import SendSESEmail


@monitors.name('Error count')
class ErrorCountMonitor(Monitor):

    @monitors.name('No errors in job')
    def test_no_errors(self):
        error_count = getattr(self.data.stats, 'log_count/ERROR', 0)

        self.assertTrue(error_count > 0, msg='We have errors yo!')

    @monitors.name('Items dropped')
    def test_no_items_dropped(self):
        drop_count = getattr(self.data.stats, 'item_dropped_count', 0)

        self.assertTrue(
            drop_count > 0, msg='We have drops yo! Check the schema!')

class SpiderCloseMonitorSuite(MonitorSuite):

    monitors = [
        ErrorCountMonitor,
    ]

    # TODO: Configure aws email notifications
    # monitors_finished_actions = [
    #     SendSESEmail,
    # ]