import wixLocation from 'wix-location';
import wixAnimations from 'wix-animations';

$w.onReady(function () {
    // Initially hide the searchbuttonDisplay and the HTML component
    $w("#searchbuttonDisplay").hide();
    $w("#html1").hide();

    // Start the loading spinner animation
    const spinnerAnimation = wixAnimations.timeline({ repeat: -1 });
    spinnerAnimation.add($w("#loadingSpinner"), { rotate: 360, duration: 1000, easing: 'easeLinear' }).play();

    // Retrieve and decode URL query parameters
    let incomeStatement = wixLocation.query.income_statement;
    let balanceSheet = wixLocation.query.balance_sheet;
    let cfStatement = wixLocation.query.cf_statement;

    // Ensure all required financial statements are present
    if (incomeStatement && balanceSheet && cfStatement) {
        // Construct the URL for the iframe src using the decoded query parameters
        let reportUrl = `https://equitary-reports.ngrok.io/generate_economic_report?income_statement_text=${incomeStatement}&balance_sheet_text=${balanceSheet}&cash_flow_statement_text=${cfStatement}`;
        $w("#html1").src = reportUrl;

        // Listen for a message indicating that the report is ready
        $w("#html1").onMessage((event) => {
            if (event.data.status === 'loaded') {
                // Stop the spinner and display the report and the search button
                spinnerAnimation.pause();
                $w("#loadingSpinner").hide();
                $w("#html1").show();
                $w("#searchbuttonDisplay").show();
            }
        });
    } else {
        // Redirect to an error page if any of the financial statements are missing
        wixLocation.to('/no-ticker-found');
    }
});
