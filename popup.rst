pdf to text in popup
====================


the user can upload a pdf file and have it converted to text on the fly.
After a quick checkup of the text, further actions take place



Explanation

-    HTML Form: The form allows the user to upload a PDF file.
-    JavaScript (AJAX): When the form is submitted, JavaScript sends the file to the Flask /upload route using AJAX, so the page doesn’t refresh.
-    Modal Popup: On a successful response, the extracted text is inserted into a <pre> tag within the modal, and the modal is displayed.
-    Bootstrap: The modal popup is styled with Bootstrap, making it easy to integrate and visually appealing.

Now, when you upload a PDF through the form, the extracted text will appear in a popup modal.
