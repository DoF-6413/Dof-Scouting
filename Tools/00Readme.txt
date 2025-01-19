These are the various tools you need to run the app or to do 'stuff' like create random data to test with.

To run the app locally, you need to install the Rebex Tiny Web Server.  The server is extremely simple to use. Just unpack the ZIP file, run the executable, and that's all. 

NOTE: Tiny Web Server is meant for testing and debugging purposes only. It is not intended for Internet-facing endpoints like the teams web site!!

The current version as of the creation of this file is 1.0.0 (2022-02-22).  It is available in this directory in the RebexTinyWebServer-Binaries-Latest.zip file.  If you prefer you can download your own copy from https://www.rebex.net/tiny-web-server/

To install and run just do the following:

Download and unpack the ZIP package.
Optional: edit RebexTinyWebServer.exe.config.
Run RebexTinyWebServer.exe
Press Start button to begin serving files via HTTP/HTTPS.

Configuration
The server can be configured using RebexTinyWebServer.exe.config file. This configuration file must be placed in the same folder as the executable file.

httpPort
TCP port on which the server listens for HTTP connections. If not specified, the HTTP is disabled.

httpsPort
TCP port on which the server listens for HTTPS connections. If not specified, the HTTPS is disabled.

webRootDir
Root data folder. If the folder does not exist, the server creates it and puts some test data there. Default is ./wwwroot.

defaultFile
Default file to be sent if the request URL points to a directory. Default is index.html.

serverCertificateFile
Path to the server certificate with associated private key. PKCS #12 (.pfx file extension) format is supported. A new self-signed certificate is generated if it does not exist:

.pfx file is intended to be used on the server.
.cer file is intended to be installed on the client into the "Trusted Root Certification Authorities" store.

For more information, read our Introduction to Public Key Certificates. Default is server-certificate.pfx.

serverCertificatePassword
Password for the server certificate.

autoStart
If set to true, the server starts when application is started. No need to press the button. Default is false.

Note:
To minimize possible "port in use" conflict, the initial values of ports are assigned to 1180 for HTTP and 11443 for HTTPS. If you need to test your web client with standard ports, please modify httpPort and httpsPort in the configuration file to 80 for HTTP and 443 for HTTPS and make sure there is no other service using those ports.