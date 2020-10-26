from nose2.tools import such


from diary.models import DiaryId
from page.models import Page


with such.A('Page') as it:

    @it.should('do create')
    def test_create(case):
        page = Page.create(DiaryId('1'), Lang.Ja, '本日は晴天なり')
        case.assert_(isinstance(page, Page))


it.createTests(globals())
