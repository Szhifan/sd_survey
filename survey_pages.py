from typing import Union

import streamlit as st

js_script_to_top = """
<script>
    var body = window.parent.document.querySelector(".main");
    console.log(body);
    body.scrollTop = 0;
</script>

"""
class Pages(object):

    @staticmethod
    def default_btn_previous(label="Previous"):
        return lambda pages: st.button(
            label,
            use_container_width=True,
            on_click=pages.previous,
            disabled=pages.current == 0,
            key=f"{pages.current_page_key}_btn_prev",
        
        )

    @staticmethod
    def default_btn_next(label="Next"):
        return lambda pages: st.button(
            label,
            use_container_width=True,
            on_click=pages.next,
            disabled=(pages.current == pages.n_pages - 1) or (not pages.proceed_to_next),
            key=f"{pages.current_page_key}_btn_next",

        )
    @staticmethod
    def default_btn_jump(label="jump to latest"):
        return lambda pages : st.button(
            label,
            use_container_width=True,
            on_click=pages.latest,
            disabled=pages.current == pages.n_pages - 1, 
            key=f"{pages.current_page_key}_btn_jump", 
        )
    @staticmethod
    def default_btn_submit(label="Submit"):
        return lambda pages: st.button(label, use_container_width=True, key=f"{pages.current_page_key}_btn_next")

    def __init__(self, labels: Union[int, list],key="__Pages_curent", on_submit=None, progress_bar=False):
        """
        Parameters
        ----------
        labels: int
            Number of pages
        key: str
            Key to use to store the current page in Streamlit's session state
        on_submit: Callable
            Callback to call when the user clicks the submit button
        progress_bar: bool
            Whether to show a progress bar under the survey buttons. Default is False.

        Example
        -------
        >>> page = Pages(2)
        >>> with page:
        >>>     if page.current == 0:
        >>>         st.text_input("Email address:", id="email")
        >>>     if page.current == 1:
        >>>         st.text_input("Phone number:", id="phone")
        """
        if isinstance(labels, int):
            labels = list(range(labels))
        self.n_pages = len(labels)
        self.proceed_to_next = True
        self.allow_submit = False
        self.labels = labels 
        self.current_page_key = key
        self.on_submit = on_submit
        self.progress_bar = progress_bar
        self.latest_page = 0 
        self.next_func = lambda : None
        self._prev_btn = Pages.default_btn_previous()
        self._next_btn = Pages.default_btn_next()
        self._submit_btn = Pages.default_btn_submit()
        self._jump_btn = Pages.default_btn_jump()

    def update(self, value):
        """
        Update current page index value.

        Parameters
        ----------
        value: int
            Page index.
        """
        self.current = value
    

    @property
    def current(self):
        """
        Returns
        -------
        int:
            Current page
        """
        if self.current_page_key not in st.session_state:
            st.session_state[self.current_page_key] = 0
        return st.session_state[self.current_page_key]

    @current.setter
    def current(self, value):
        """
        Parameters
        ----------
        value: int
            Current page

        Raises
        ------
        ValueError:
            If the value is out of range
        """
        if value >= 0 and value < self.n_pages:
            st.session_state[self.current_page_key] = value
        else:
            raise ValueError("Page index out of range")
    @property
    def label(self):
        return self.labels[self.current]

    def previous(self):
        """
        Go to the previous page
        """
        if self.current > 0:
            self.current -= 1

    def next(self):
        """
        Go to the next page
        """
        if self.current < self.n_pages - 1:
            self.current += 1
    def latest(self):
        """
        jump to the latest page
        """
   
        self.current = self.latest_page 

    @property
    def prev_button(self):
        """
        Returns "previous" button for page navigation.
        """
        return self._prev_btn(self)

    @prev_button.setter
    def prev_button(self, func):
        """
        Set "previous" button for page navigation. Use the `key_btn_prev()` method to create the button's key string.

        Parameters
        ----------
        func: function
            Function taking one argument (the current page instance) and returning the "previous" button for page navigation.
        """
        self._prev_btn = func

    @property
    def next_button(self):
        """
        Returns "next" button for page navigation.
        """
        return self._next_btn(self)

    @next_button.setter
    def next_button(self, func):
        """
        Set "next" button for page navigation. Use the `key_btn_next()` method to create the button's key string.

        Parameters
        ----------
        func: function
            Function taking one argument (the current page instance) and returning the "next" button for page navigation.
        """
        self._next_btn = func

    @property
    def submit_button(self):
        """
        Returns "submit" button for page navigation.
        """
        return self._submit_btn(self)

    @submit_button.setter
    def submit_button(self, func):
        """
        Set "submit" button for page navigation. Use the `key_btn_submit()` method to create the button's key string.

        Parameters
        ----------
        func: function
            Function taking one argument (the current page instance) and returning the "submit" button for page navigation.
        """
        self._submit_btn = func
    @property
    def jump_button(self):
        """
        return "jump to latest" button to the last annotated example.
        """
        return self._jump_btn(self)
    @jump_button.setter
    def jump_button(self,func):
        self._jump_btn = func

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """
        Display the navigation buttons
        """
        submitted = False
        left, _,mid,_, right = st.columns([2,1,2,1, 2])
        with left:
            prev  = self.prev_button
            if prev:
                st.components.v1.html(js_script_to_top)
        with right:
            if self.current == self.n_pages - 1 and self.on_submit is not None:
               
                submitted = self.submit_button if self.allow_submit else None
            else:
                next = self.next_button
                if next:
                    proceed = self.next_func()
                    # if not proceed:
                    #     self.proceed_to_next = False

                    st.components.v1.html(js_script_to_top)
        with mid:
            if self.latest_page:
                self.jump_button
        if self.progress_bar and self.n_pages > 1:
            st.progress(self.current / (self.n_pages - 1))
        if submitted:
            self.on_submit()
