class Resource:
    def __init__(self, resource_name, resource_url,
                top_tag, bottom_tag,  title_cut, date_cut):
        # self.RESOURCE_ID = RESOURCE_ID
        self.RESOURCE_NAME = resource_name
        self.RESOURCE_URL = resource_url
        self.top_tag = top_tag
        self.bottom_tag = bottom_tag
        self.title_cut = title_cut
        self.date_cut = date_cut

class Items:
    def __init__(self,res_id, link, title, content, nd_date, s_date, not_date):
        self.res_id = res_id
        self.link = link
        self.title = title
        self.content = content
        self.nd_date = nd_date
        self.s_date = s_date
        self.not_date = not_date