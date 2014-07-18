button_style = '''QPushButton {
     border: 1px solid #C4C4C4;
     border-radius: 8px;
     padding: 2px;
 }
 QPushButton:hover {
     background: #C4C4C4;
 }'''

editor_style = '''QTextEdit{
     border: 1px solid #C4C4C4;
     border-radius: 4px;
     padding: 2px;
 }'''

shell_style = '''QTextEdit{
     min-width: 20%;
     border: 1px solid #C4C4C4;
     border-radius: 4px;
     padding: 2px;
     background-color: #000000;
     color: #ffffff;
 }'''

browser_style = '''QWebView{
     border: 1px solid #C4C4C4;
     border-radius: 4px;
     padding: 2px;
}'''

tab_style = '''
 QTabWidget::pane { /* The tab widget frame */
     border: 1px solid  #C4C4C4;
     border-radius: 4px;
     position: absolute;
     top: -0.5em;
 }
 QTabBar::tab {
     background-color: #C4C4C4;
     border: 1px solid  #C4C4C4;
     border-bottom-color: #C4C4C4; /* same as the pane color */
     border-top-left-radius: 4px;
     border-top-right-radius: 4px;
     min-width: 30ex;
 }

 QTabBar::tab:selected, QTabBar::tab:hover {
     background-color: #fafafa;
 }

 QTabBar::tab:selected {
     background-color: #FFFFFF;
     border-bottom-color: #FFFFFF;
 }'''
