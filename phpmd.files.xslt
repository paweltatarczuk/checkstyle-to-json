<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" 
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output indent="no" method="text" omit-xml-declaration="yes" />

	<xsl:template match="pmd">
		<xsl:for-each select="file">
			<xsl:value-of select="@name" />
			<xsl:text>&#xa;</xsl:text>
		</xsl:for-each>
	</xsl:template>
</xsl:stylesheet>