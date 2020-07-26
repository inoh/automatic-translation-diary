from nose2.tools import such


from diary.models import Diary
from page.models import Page


with such.A('Diary') as it:

    @it.should('do create')
    def test_create(case):
        diary = Diary.create()
        case.assert_(isinstance(diary, Diary))


    @it.should('do write')
    def test_write(case):
        diary = Diary.create()
        page = diary.write('本日は晴天なり')
        case.assert_(isinstance(page, Page))


it.createTests(globals())
