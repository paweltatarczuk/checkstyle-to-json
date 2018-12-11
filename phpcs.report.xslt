<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" 
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output indent="no"/>
	
	<xsl:template match="checkstyle">
		<xsl:element name="report">
			<xsl:apply-templates />
		</xsl:element>
	</xsl:template>

	<xsl:template match="file">
		<xsl:variable name="filePath" select="@name" />
		
		<xsl:for-each select="error">
			<xsl:element name="violation">
				<xsl:attribute name="severity"><xsl:value-of select="@severity" /></xsl:attribute>
				<xsl:attribute name="message"><xsl:value-of select="@message" /></xsl:attribute>
				<xsl:attribute name="rule"><xsl:value-of select="@source" /></xsl:attribute>
				<xsl:attribute name="file"><xsl:value-of select="$filePath" /></xsl:attribute>
				<xsl:attribute name="line"><xsl:value-of select="@line" /></xsl:attribute>
			</xsl:element>
		</xsl:for-each>
	</xsl:template>
</xsl:stylesheet>