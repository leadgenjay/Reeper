.PHONY: test validate export

test:
	python3 -m unittest discover -s tests -v

validate:
	python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
	python3 -m json.tool plugins/reeper/.claude-plugin/plugin.json >/dev/null
	python3 -m unittest discover -s tests -v

export:
	python3 scripts/export_marketplace_skill.py
