<?xml version="1.0" encoding="UTF-8"?>

 <!-- XSLT namespace declaration -->
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

	<!-- Output settings -->
    <xsl:output method="html" indent="yes" encoding="UTF-8" />

	<!-- ROOT TEMPLATE: Matches the root node of the XML document -->
    <xsl:template match="/">
        <html>
        <head>
            <title>Bookshop Catalogue</title>
            <style>
				<!-- Set consistent font family for all text elements -->
                body, td, th, a, h2, h1 {
					font-family: Trebuchet MS, sans-serif;
                }
				<!-- Body styling with background image -->
				body {
                   margin: 0;
                   background-image: url('xml_background.jpg');
                   background-size: cover;
                   background-attachment: fixed;
                   background-repeat: no-repeat;
                   background-position: center;
                   position: relative;
				   overflow-x: hidden;
                }

               body::before {
                   content: ""; <!-- Required fir pseudo-element -->
                   position: fixed; <!-- Fixed position overlay -->
                   top: 0;
                   left: 0;
                   width: 100%;
                   height: 100%;
                   background: #00000040;
                   z-index: -1; <!-- Place behind content -->
                }

				<!-- ===== CONTACT BAR (same styles as css) -->
				.contact-bar {
					background: #BB9944;
					color: white;
					width: 100%;
					table-layout: fixed;
					border-collapse: collapse;
				}

				.contact-bar td {
					padding: 10px 5px;
					color: white;
					white-space: nowrap;
					text-align: center;
					width: 16.66%;
					border: none;
					border-radius: 0;
					font-size: 14px;
				}

				.contact-bar a {
					color: white;
					text-decoration: none;
					padding: 5px 10px;
					transition: all 0.3s ease;
					display: inline-block;
					border-radius: 0;
				}

				.contact-bar a:hover {
					background-color: rgba(255, 255, 255, 0.2);
					border-radius: 4px;
					text-decoration: underline;
					transform: translateY(-2px);
				}
				
				<!-- ===== Main header (same styles as css) -->
				.main-header {
					background: #CC9933;
					color: white;
					margin-bottom: 0;
				}

				.main-header h1 {
					color: white;
					display: inline;
					position: relative;
					bottom: 35px;  
				}
				
				.main-header img {
					position: static;
				}
				

                .return-button {
				   display: inline-block;
                   padding: 12px 20px;
                   border: 2px solid #5a432c;
                   border-radius: 8px;
                   background-color: #BB9944;
                   font-weight: 600;
                   color: #5a432c;
                   text-decoration: none;
				   margin-right: 10px;
                }

                .return-button:hover {
                   background-color: #b8862b;
                }
				
				<!-- Navigation Bar -->
				.nav-table {
					display: table; <!-- Table layout -->
					width: 100%;
					border-collapse: collapse;
					background-color: #CC9933;
				}

				.nav-table td {
					padding: 0px 0px 5px 0px; <!-- Bottom padding only -->
					position: relative;
				}

				<!-- Navigation Items (Categories, Coming soon... -->
				.nav-item {
					font-size: 18px;
					font-weight: 600;
					color: #fff;
					cursor: pointer;
					text-align: center;
					position: relative;
				}
				
				<!-- Dropdown arrow indicator -->
				.arrow {
					margin-left: 6px; <!-- Space between text and arrow -->
					font-size: 14px;
				}

				<!-- Dropdown menu styles -->
				.dropdown {
					display: none; <!-- Hidden by default -->
					position: absolute; <!-- Position relative to nav item -->
					top: 100%; <!-- Below nav item -->
					left: 0;
					background: #FFFFFFE6;
					border-radius: 8px;
					padding: 10px;
					min-width: 150px;
					box-shadow: 0 3px 10px #00000047;
					z-index: 100; <!-- Dropdown appears above other content -->
				}

				.nav-item:hover .dropdown {
					display: block;
				}

				.dropdown a {
					display: block;
					padding: 8px;
					text-decoration: none;
					color: #5a432c;
				}

				.dropdown a:hover {
					background-color: #D8B58940;
				}

				<!-- Search bar styles -->
				.search-container {
					text-align: center;
				}

				.search-input {
					padding: 8px 12px;
					border: 2px solid #5a432c;
					border-radius: 6px;
					background: #fff;
					font-size: 15px;
					width: 250px;
					margin-right: 6px;
				}

				.search-btn {
					padding: 8px 12px;
					background-color: #BB9944;
					color: #5a432c;
					font-weight: 600;
					border: 2px solid #5a432c;
					border-radius: 6px;
					cursor: pointer;
					width: 100px;
				}

				.search-btn:hover {
					background-color: #D8B589FF;
				}
				
				<!-- Books table styles -->
                .books-table {
                   border-collapse: collapse;
                   width: 80%;
                   margin: 20px auto;
                   background-color: #FFFFFFE6;
                   border-radius: 12px;
                   overflow: hidden; <!-- Hides rounded corner overflow -->
                   box-shadow: 0 3px 10px #00000047;
                }

                .books-table th {
                   background-color: #CC9933;
                   color: #5a432c;
                   border-bottom: 2px solid #5a432c;
                   padding: 12px;
                   font-size: 18px;
                }

                .books-table td {
                   border: 1px solid #5a432c;
                   padding: 10px;
                   font-size: 15px;
                   color: #3D2F2A;
                }

                .books-table tr:hover {
                   background-color: #D8B58940;
                }

				<!-- Footer styles (same as css) -->
				footer {
					text-align: center;
					background: #CC9933;
					color: white;
					font-size: 16px;
					border: 2px solid #CC9933;
					width: 100%;
				}   	   
            </style>
			
        </head>

        <body>


			<!-- Contact Bar -->
			<table class="contact-bar" width="100%">
				<tr>
					<td>📞 +230 58017780</td>
					<td>✉️ info@bookstore.co.mu</td>
					<td>
						<img src="ukflag.jpg" width="16" height="10" loading="lazy" alt="UK Flag"/> English
					</td>
					<td>Currency: £</td>
					<td><a href="bookshop.html#about-us" class="top-link">About us</a></td>
					<td><a href="bookshop.html#delivery-services" class="top-link">Delivery Services</a></td>
				</tr>
			</table>

			<!-- Main Header -->
			<table class="main-header" width="100%">
				<tr>
					<td align="left" valign="middle">
						<img src="logo_book.png" alt="Logo" width="100"/>
						<h1>The Academia Bookstore</h1>
					</td>
					<td align="right" valign="middle">
						<xsl:apply-templates select="bookshop/link"/>
					</td>
				</tr>
			</table>
			
			<!-- Navigation Bar -->
			<table class="nav-table" width="100%">
				<tr>
					<!-- Categories dropdown -->
					<td width="15%" class="nav-item">
						Categories <span class="arrow">▼</span>
						<div class="dropdown">
							<a href="#">Fantasy</a>
							<a href="#">Thriller</a>
							<a href="#">Romance</a>
							<a href="#">Literacy Fiction</a>
							<a href="#">Classic</a>
							<a href="#">Inspirational</a>
							<a href="#">Dystopian</a>
						</div>
					</td>
					
					<!-- Coming soon dropdown -->
					<td width="15%" class="nav-item">
						Coming Soon <span class="arrow">▼</span>
						<div class="dropdown">
							<a href="#">Harry Potter and The Chamber Of Secrets</a>
							<a href="#">Twilight</a>
							<a href="#">Twisted Love</a>
							<a href="#">The Haunting of Hill House</a>
						</div>
					</td>
					
					<!-- Find us on dropdown -->
					<td width="15%" class="nav-item">
						Find us on <span class="arrow">▼</span>
						<div class="dropdown">
							<a href="#">Instagram</a>
							<a href="#">Facebook</a>
							<a href="#">Twitter</a>
						</div>
					</td>
					
					<!-- Empty spacer column -->
					<td width="15%"></td>
					
					<!-- Search Bar -->
					<td width="40%" class="search-container" align="center">
						<input type="text" placeholder="Search books..." class="search-input"/>
						<button class="search-btn">Search</button>
					</td>
				</tr>
			</table>			
			
			<!-- Spacer div for visual separation -->
			<div style="height: 20px;"></div>
			
			 <!-- Books Catalogue Table:  populated from XML data -->
            <table class="books-table">
                <tr>
                    <th>Title</th>
                    <th>Author</th>
                    <th>Genre</th>
                    <th>Description</th>
                    <th>Price (£)</th>
                </tr>

				<!-- XSLT LOOP: Process each book element in the XML file -->
                <xsl:for-each select="bookshop/book">
                    <tr>
                        <td><xsl:value-of select="title"/></td>
                        <td><xsl:value-of select="author"/></td>
                        <td><xsl:value-of select="genre"/></td>
                        <td><xsl:value-of select="description"/></td>
                        <td><xsl:value-of select="price"/></td>
                    </tr>
                </xsl:for-each>
            </table>
			
			<!-- Footer: Copyright information -->
			<footer>
                <p align="center">© 2025 The Academia Bookstore. All rights reserved.</p>
            </footer>
 
        </body>
        </html>
    </xsl:template>
	
	<!--LINK TEMPLATE: Processes and matches link elements from XML -->
    <xsl:template match="link">
		<!-- Anchor tag with href from XML attribute and text from element content -->
        <a class="return-button" href="{@href}">
            <xsl:value-of select="."/>
        </a>
    </xsl:template>

</xsl:stylesheet>
