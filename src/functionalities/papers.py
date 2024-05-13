class Publication:
    def __init__(self, title, doi, cites, num_pages, publication_date, language, pages, published_in, main_subject, instance_of):
        self._title = title
        self._doi = doi
        self._cites = cites
        self._num_pages = num_pages
        self._publication_date = publication_date
        self._language = language
        self._pages = pages
        self._published_in = published_in
        self._main_subject = main_subject
        self._instance_of = instance_of

    # Getters
    def get_title(self):
        return self._title

    def get_doi(self):
        return self._doi

    def get_cites(self):
        return self._cites

    def get_num_pages(self):
        return self._num_pages

    def get_publication_date(self):
        return self._publication_date

    def get_language(self):
        return self._language

    def get_pages(self):
        return self._pages

    def get_published_in(self):
        return self._published_in

    def get_main_subject(self):
        return self._main_subject

    def get_instance_of(self):
        return self._instance_of

    # Setters
    def set_title(self, title):
        self._title = title

    def set_doi(self, doi):
        self._doi = doi

    def set_cites(self, cites):
        self._cites = cites

    def set_num_pages(self, num_pages):
        self._num_pages = num_pages

    def set_publication_date(self, publication_date):
        self._publication_date = publication_date

    def set_language(self, language):
        self._language = language

    def set_pages(self, pages):
        self._pages = pages

    def set_published_in(self, published_in):
        self._published_in = published_in

    def set_main_subject(self, main_subject):
        self._main_subject = main_subject

    def set_instance_of(self, instance_of):
        self._instance_of = instance_of

    #Other fucntions
    def display_info(self):
        print("Title:", self._title)
        print("DOI:", self._doi)
        print("Cites:", self._cites)
        print("Number of Pages:", self._num_pages)
        print("Publication Date:", self._publication_date)
        print("Language:", self._language)
        print("Pages:", self._pages)
        print("Published In:", self._published_in)
        print("Main Subject:", self._main_subject)
        print("Instance Of:", self._instance_of)

