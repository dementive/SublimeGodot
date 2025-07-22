import sublime
import sublime_plugin

import os
import xml.etree.ElementTree as ET

def to_markdown(text: str):
	text = text.replace('[b]', '**').replace('[/b]', '**')
	text = text.replace('[i]', '*').replace('[/i]', '*')
	text = text.replace('[kbd]', '- ').replace('[/kbd]', '')
	text = text.replace('[code]', '`').replace('[/code]', '`')
	text = text.replace('[code skip-lint]', '`').replace('[/code skip-lint]', '`')

	# Handle code blocks
	start_code_block = text.find('[codeblocks]')
	end_code_block = text.find('[/codeblocks]', start_code_block)

	if start_code_block != -1 and end_code_block != -1:
		code_block_content = text[start_code_block:end_code_block]
		code_block_markdown = f'{code_block_content}'.replace("[codeblocks]", "")
		code_block_markdown = code_block_markdown.replace("[gdscript]", "```gdscript")
		code_block_markdown = code_block_markdown.replace("[gdscript skip-lint]", "```gdscript")
		code_block_markdown = code_block_markdown.replace("[/gdscript]", "```")
		# code_block_markdown = code_block_markdown.replace("[csharp skip-lint]", "```csharp")
		# code_block_markdown = code_block_markdown.replace("[csharp]", "```csharp")
		# code_block_markdown = code_block_markdown.replace("[/csharp]", "```")
		text = text[:start_code_block] + code_block_markdown + text[end_code_block:]
		text = text.replace("[/codeblocks]", "")

	text = text.replace("[codeblock]", "```gdscript")
	text = text.replace("[/codeblock]", "```")
	text = text.replace("[codeblock lang=text]", "```gdscript")

	return text

class GodotClassDocumentation:
	def __init__(self, root_xml_element : ET.Element):
		self.root = root_xml_element

		# Class info
		self.class_name = ""
		self.inherits_from = ""
		self.brief_description = ""
		self.full_description = ""

		# Tutorial info
		self.tutorials = [] # [{"title": "name", "link": "https://link.com"}]

		# Signal info
		self.signals = [] # [{"name": "signal_name", "description": "My signal desc"}]

		# Methods info
		self.methods = []

		# Members info
		self.members = []

		# Constants info
		self.constants = []

		self.get_class_info()
		self.get_tutorial_info()
		self.get_signal_info()
		self.get_methods_info()
		self.get_members_info()
		self.get_constants_info()


	def get_default(self, item: str) -> str:
		if item:
			return f", Default - {item}"
		else:
			return ""

	def get_link(self, item: str) -> str:
		settings = sublime.load_settings("SublimeGodot.sublime-settings")
		docs_url = settings.get("DocsURL") # type: str

		if item:
			return item.replace("$DOCS_URL", docs_url)
		else:
			return ""

	def remove_leading_underscores(self, input_string: str):
		lines = input_string.split("\n")
		out_lines = ""

		ignore = False

		for line in lines:
			if line.__contains__("[codeblock]") or line.__contains__("[csharp]") or line.__contains__("[csharp skip-lint]"):
				ignore = True
			if line.__contains__("[/codeblock]") or line.__contains__("[/csharp]"):
				ignore = False
				continue

			if ignore:
				continue

			words = line.split()
			modified_words = []
			
			needs_modification = any(word.startswith('_') for word in words)

			if needs_modification:
				for word in words:
					if word.startswith('_'):
						modified_words.append(word.lstrip('_'))
					else:
						modified_words.append(word)
				out_lines += "\n" + ' '.join(modified_words)
			else:
				out_lines += "\n" + line

		return out_lines


	def generate_markdown(self):
		markdown_content = ""
		markdown_content += f"# {to_markdown(self.class_name)}"
		markdown_content += f"{to_markdown(self.inherits_from)}\n"
		markdown_content += f"{to_markdown(self.brief_description)}\n"
		markdown_content += f"{to_markdown(self.full_description)}\n"

		# Tutorials
		tutorials_md = "\n".join([f"[{to_markdown(item['title'])}]({self.get_link(item['link'])})" for item in self.tutorials])
		
		# Signals
		signals_md = "\n".join([f"- **{to_markdown(item['name'])}**: {to_markdown(item['description'])}" for item in self.signals])
		
		# Methods
		methods_md = ""
		for item in self.methods:
			methods_md += f"## {to_markdown(item['name'])}"
			methods_md += f"{to_markdown(item['description'])}\n\n"
			if len(item["parameters"]) > 0:
				methods_md += "### Parameters\n"
				for param in item["parameters"]:
					default_value = f"= {to_markdown(param['default'])}" if param['default'] else ""
					enum_value = f"- Enum: {to_markdown(param['enum'])}" if param['enum'] else ""
					methods_md += f"- `{to_markdown(param['name'])}`: {to_markdown(param['type'])} {default_value} {enum_value}\n\n"
				
		# Members
		members_md = "\n".join([f"- **{to_markdown(item['name'])}**: Type - {to_markdown(item['type'])}{self.get_default(to_markdown(item['default_value']))}" for item in self.members])
		
		# Constants
		constants_md = "\n".join([f"- **{to_markdown(item['name'])}**: Value - {to_markdown(item['value'])}" for item in self.constants])

		# Combine everything into one Markdown string
		markdown_content = f"# {to_markdown(self.class_name)}\n\n{to_markdown(self.inherits_from)}\n\n## Brief Description\n{to_markdown(self.brief_description)}\n\n## Full Description\n{to_markdown(self.full_description)}\n\n## Tutorials\n{tutorials_md}\n\n## Signals\n{signals_md}\n\n## Methods\n{methods_md}\n\n## Members\n{members_md}\n\n## Constants\n{constants_md}"

		# Trim leading and trailing whitespace from each line
		markdown_content = "\n".join(line for line in markdown_content.split("\n"))

		# Replace double spaces with a single space to prevent extra spacing in rendered Markdown
		markdown_content = markdown_content.replace("  ", " ")
		markdown_content = self.remove_leading_underscores(markdown_content)

		return markdown_content

	def get_class_info(self):
		self.class_name = self.root.attrib['name']
		try:
			self.inherits_from = self.root.attrib['inherits']
		except KeyError:
			self.inherits_from = ""

		desc = self.root.find('brief_description')
		if desc is not None and desc.text:
			self.brief_description = desc.text

		desc = self.root.find('description')
		if desc is not None and desc.text:
			self.full_description = desc.text

	def get_tutorial_info(self):
		tutorials = self.root.find('tutorials')
		if tutorials is None:
			return
		for link in tutorials.findall('link'):
			title = link.attrib['title']
			if link.text:
				url = link.text
				self.tutorials.append({
					"title": title,
					"link": url
				})

	def get_signal_info(self):
		signals = self.root.find('signals')
		if signals is None:
			return
		for signal in signals.findall('signal'):
			name = signal.attrib['name']
			descriptions = signal.find('description')
			if descriptions is not None and descriptions.text:
				description = descriptions.text
				self.signals.append({
					"name": name,
					"description": description
				})

	def get_methods_info(self):
		methods = self.root.find('methods')

		if methods is None:
			return

		for method in methods.findall('method'):
			method_name = method.attrib['name']
			return_type_xml = method.find('return')
			return_type = ""
			description = ""

			if return_type_xml is not None:
				return_type = return_type_xml.attrib.get('type', '')


			desc = method.find('description')
			if desc is not None and desc.text:
				description = desc.text

			params = method.findall('param')
			parameters = []
			for param in params:
				index = param.attrib['index']
				name = param.attrib['name']
				type_ = param.attrib['type']
				default_value = param.attrib.get('default', '')
				enum = param.attrib.get('enum', '')

				parameters.append({
					"index": index,
					"name": name,
					"type": type_,
					"default": default_value,
					"enum": enum
				})

			self.methods.append({
				"name": method_name,
				"return_type": return_type,
				"description": description,
				"parameters": parameters,
			})

	def get_members_info(self):
		members = self.root.find('members')

		if members is None:
			return

		for member in members.findall('member'):
			name = member.attrib['name']
			type_ = member.attrib['type']
			setter = member.attrib.get('setter', '')
			getter = member.attrib.get('getter', '')
			enum = member.attrib.get('enum', '')
			default_value = member.attrib.get('default', '')
			description = ""
			if member.text:
				description = member.text

			self.members.append({
				"name": name,
				"type": type_,
				"setter": setter,
				"getter": getter,
				"enum": enum,
				"default_value": default_value,
				"description": description,
			})

	def get_constants_info(self):
		constants = self.root.find('constants')

		if constants is None:
			return

		for constant in constants.findall('constant'):
			name = constant.attrib['name']
			value = constant.attrib['value']
			enum = constant.attrib.get('enum', '')
			description = ""
			if constant.text:
				description = constant.text

			self.constants.append({
				"name": name,
				"value": value,
				"enum": enum,
				"description": description,
			})

class GodotDocsListInputHandler(sublime_plugin.ListInputHandler):
	def name(self):
		return "doc_class"

	def list_items(self):
		settings = sublime.load_settings("SublimeGodot.sublime-settings")
		godot_docs_path = settings.get("GodotDocumentationPath") # type: str
		godot_docs = os.listdir(godot_docs_path)
		items = []
		for doc in godot_docs:
			items.append(doc.replace(".xml", ""))

		return items

class ShowGodotDocsMarkdownCommand(sublime_plugin.WindowCommand):

	def input_description(self):
		return "Select Class Documentation"

	def input(self, args):
		if "doc_class" not in args:
			return GodotDocsListInputHandler()

	def run(self, doc_class):
		settings = sublime.load_settings("SublimeGodot.sublime-settings")
		godot_docs_path = settings.get("GodotDocumentationPath")

		with open(f"{godot_docs_path}/{doc_class}.xml", "r") as file:
			xml_string = file.read()
		root_xml_element = ET.fromstring(xml_string)
		docs = GodotClassDocumentation(root_xml_element)

		markdown = docs.generate_markdown()
		markdown_lines = markdown.splitlines(True)
		markdown_str = ""
		ignore_strip = False

		for line in markdown_lines:
			if line.startswith("\t\t\t"):
				pass

			stripped = line.strip()

			if stripped.__contains__("```"):
				markdown_str += stripped + "\n"
				ignore_strip = not ignore_strip
			elif ignore_strip:
				markdown_str += line
				markdown_str = markdown_str.replace("\t\t\t\t", "")
			else:
				markdown_str += stripped + "\n"

		markdown_str = markdown_str.replace("\n\n\n\n", "\n\n")
		markdown_str = markdown_str.replace("\n\n\n###", "\n\n###")
		markdown_str = markdown_str.replace("\n# ", "# ")

		with open(f"{sublime.cache_path()}/{doc_class}.md", "w") as file:
			file.write(markdown_str)

		view = self.window.open_file(f"{sublime.cache_path()}/{doc_class}.md")
		view.assign_syntax("scope:text.html.markdown.godot")
		view.set_scratch(True)
		view.set_read_only(True)
		view.set_name(doc_class)
