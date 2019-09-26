var id = "spreadsheet_id_here"  // Replace with spreadsheet id


function buildEmail(data) {
  //var todaysDate = Utilities.formatDate(new Date(), "EST", "MM/dd/yyyy");
  var htmlBody = HtmlService.createTemplateFromFile("template");

  htmlBody.lastName = data[0];
  htmlBody.firstName = data[1]
  htmlBody.address = data[4];
  htmlBody.city = data[5];
  htmlBody.state = data[7];
  htmlBody.zip = data[6];
  htmlBody.loanAmount = data[3];
  htmlBody.dateReceived = data[2]; // Need to verify formatting

  return htmlBody
}


function sendEmail(htmlBody, emailAddress) {
  // Evaluate and get the html string
  var emailHtml = htmlBody.evaluate().getContent();

  // Send the email
  MailApp.sendEmail({
    to: emailAddress,
    subject: "Coker College - Notice of Right of Loan Cancellation",
    htmlBody: emailHtml
  });
}


function main() {
  var ss = SpreadsheetApp
  .openById(id)
  .getSheetByName('data');
  var data = ss.getDataRange()
  .getValues();

  for (i = 1; i < data.length; i++) {
    // Check if email has already been sent
    if (data[i][9] != "yes") { // If not...
      Logger.log("Sending email...")
      // Create email contents
      var htmlBody = buildEmail(data[i]);

      // Split email string into separate emails
      var emails = data[i][8].split('|')

      // Send email(s)
      emails.forEach(function(emailAddress) {
        sendEmail(htmlBody, emailAddress);
      });

      // Set the "Sent?" flag
      ss.getRange(i+1, 10)
      .setValue("yes")
    }
  }
}
