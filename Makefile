init:
	pip install pipenv --upgrade
	pipenv install --dev

test:
	ifdef DJANGO_VERSION
		pip install django==$(DJANGO_VERSION)
	fi

	pipenv run py.test tests
