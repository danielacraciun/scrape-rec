from spidermon import Monitor, MonitorSuite, monitors


@monitors.name('Error count')
class ErrorCountMonitor(Monitor):

    @monitors.name('No errors in job')
    def test_no_errors(self):
        error_count = getattr(self.data.stats, 'log_count/ERROR', 0)

        self.assertFalse(error_count > 0, msg=f'There are {error_count} errors')

    @monitors.name('Items dropped')
    def test_no_items_dropped(self):
        drop_count = getattr(self.data.stats, 'item_dropped_count', 0)

        self.assertFalse(drop_count > 0, msg=f'There are {drop_count} items dropped')


class SpiderCloseMonitorSuite(MonitorSuite):

    monitors = [
        ErrorCountMonitor,
    ]
