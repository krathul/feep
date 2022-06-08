# GUDE Power Control Sampling Information

## Summary

Info from order@gude-systems.com (GUDE Systems GmbH). Hat tip to Arne at Green Coding Berlin for sharing.

According to Gude's support, the hardware does integration of the energy result with results measured at 8 kHz. Power measurements are internally more often sampled (at least 3 times) than the output resolution of 1s. This information appears not to be in the technical manual.

## Details

Q: Die Einheit auf dem Display des GUDE Power Control scheint Watt zu sein. Über die API ist es also möglich den Wert in Watt-Sekunden (Joule) zu erhalten? Falls ja: Wird das Signal analog integriert oder digital?

A: Unsere Produkte mit Energiemessung verwenden folgenden Chip für die Messung:

 * Microchip/Atmel M90E26 Single-Phase High-Performance Wide-Span Energy Metering IC

Dieser Chip sampelt Spannung und Strom mit 8kHz und berechnet daraus Urms, Irms, Leistungs und Energiewerte. Die Energiemessung ist lückenlos und integriert intern digital alle Messwerte. Die Urms, Irms und Leistungswerte werden ca. 3-mal pro Sekunde über mehrere Perioden der Netzspannung von dem Chip berechnet. Unsere Firmware liest diese Werte jedoch nur 1 x pro Sekunde aus und stellt die Werte dann über Ihre APIs (Webseite, json, snmp, ...) zur Verfügung. Die von außen zugreifbare (APIs) Auflösung der Energiemessung ist 1Wh, d.h. es ist leider nicht möglich, den Wert in Watt-Sekunden zu bekommen.
