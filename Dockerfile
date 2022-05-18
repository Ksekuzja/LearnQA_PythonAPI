FROM python
WORKDIR /tests_project/
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV ENV=dev
CMD pyton -m pytest -s --alluredir=test_results/ /tests_project/tests/