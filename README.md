# 23
Using unittest framework and Selenium for testing an online store website.

The file 23andMe_online_purchase_smoke_test.py implements the solution.

The test performs the following 4 tasks:<br>
1. Add 3 health+ancestry and 2 ancestry only kits to the cart and verify that the kit count was correctly updated;<br>
2. Give unique names to the kits and verify that they has been successfully recorded;<br>
3. Add shipping info and check that VT -> CA correction has been done during verification;<br>
4. Continue to the payment page and verify that it was reached.

The test can be run in verbose mode from the command line as:<br>
<i>python 23andMe_online_purchase_smoke_test.py –v</i>

Note 1: path_to_chromedriver variable needs to be changed for your location of the driver<br>
Note 2: make sure that selenium and unittest modules are available in your python installation

<b>Environment used for coding</b>

1. Python=3.5.2<br>
2. Selenium=2.53.6<br>
3. chromedriver2.27.440174<br>
4. unittest (https://docs.python.org/3.5/library/unittest.html)<br>
5. chrome=55.0.2883.87<br>
6. Windows 7 Service Pack 1<br>

<b>Console printout example</b>

C:\Users\Leon\python>python 3andMe_online_purchase_smoke_test.py -v<br>
test (__main__.OnlinePurchaseSmoke)<br>
Add kits, name them, add shipping info, go to payment page ...<br>

INFO:The ordering page is opened.<br>
INFO:Adding 3 health+ancestry and 2 ancestry only kits.<br>
INFO:Giving customer#n names to kits.<br>
INFO:3 health+ancestry and 2 ancestry only kits have been added.<br>
INFO:Kits has been successfully assigned customer#n names.<br>
INFO:Continuing to shipping info input page.<br>
INFO:Continuing to shipping info verification page.<br>
INFO:Correct verified address has been suggested (CA instead of VT).<br>
INFO:Continuing to payment page.<br>
INFO:Payment page has been reached. Testing is completed.<br>
ok<br>
----------------------------------------------------------------------<br>
Ran 1 test in 52.737s<br>
OK

<b>Limitations</b>

The verifications are minimal and are meant to serve as an example of their implementation rather than of appropriately testing the online store. Their extent and single-file and single-class implementation would be somewhat appropriate for a really quick smoke test. In production environment the input of test data should be done from a YAML or JSON file.
