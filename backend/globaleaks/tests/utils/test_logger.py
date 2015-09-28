# -*- encoding: utf-8 -*-

from twisted.internet.defer import inlineCallbacks
from globaleaks.tests import helpers
from globaleaks.utils.logger import LoggedEvent, adminLog, receiverLog, \
    tipLog, LogQueue, initialize_LoggedEvent
from globaleaks.tests.jobs.test_log_sched import push_admin_logs
import pprint


class TestCollection(helpers.TestGL):

    @inlineCallbacks
    def setUp(self):
        yield helpers.TestGL.setUp(self)

    @inlineCallbacks
    def test_adminLog(self):

        yield initialize_LoggedEvent()
        logs_number = 10
        push_admin_logs(logs_number)

        x =  yield LogQueue.picklogs('admin', 50)

        pprint.pprint(x)
        self.assertTrue(len(x) == 4)


    @inlineCallbacks
    def test_receiverLog(self):
        yield initialize_LoggedEvent()
        fake_uuidv4 = 'blah-this-is-an-UUID-v4'
        other_receiver = 'CallMeOther,ButIamWorkingHardLikeEveryOtherReceiver'

        receiverLog(['mail'], 'LOGIN_3', [], fake_uuidv4)
        receiverLog(['mail'], 'LOGIN_3', [], fake_uuidv4)
        receiverLog(['mail', 'normal'], 'SECURITY_1', [], fake_uuidv4)

        receiverLog(['normal'], 'LOGIN_3', [], other_receiver)
        receiverLog(['mail', 'normal'], 'SECURITY_1', [], fake_uuidv4)

        x = yield LogQueue.picklogs(
            LogQueue.create_subject_uuid('receiver', fake_uuidv4),
            50
        )
        pprint.pprint(x)

    @inlineCallbacks
    def test_picklogs(self):

        yield initialize_LoggedEvent()
        fake_uuidv4 = 'blah-this-is-an-UUID-v4'

        adm = yield LogQueue.picklogs('admin', 10)
