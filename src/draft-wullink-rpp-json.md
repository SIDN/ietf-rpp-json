%%%
title = "JSON representation for Restful Provisioning Protocol (RPP)"
abbrev = "JSON for RPP"
ipr = "trust200902"
area = "Internet"
workgroup = "Network Working Group"
submissiontype = "IETF"
keyword = [""]
TocDepth = 4

[seriesInfo]
name = "Internet-Draft"
value = "draft-wullink-rpp-json-01"
stream = "IETF"
status = "standard"

[[author]]
initials="M."
surname="Wullink"
fullname="Maarten Wullink"
abbrev = ""
organization = "SIDN Labs"
  [author.address]
  email = "maarten.wullink@sidn.nl"
  uri = "https://sidn.nl/"

[[author]]
initials="P."
surname="Kowalik"
fullname="Pawel Kowalik"
abbrev = ""
organization = "DENIC"
  [author.address]
  email = "pawel.kowalik@denic.de"
  uri = "https://denic.de/"

%%%

.# Abstract

This document defines the rules for representing the RESTful Provisioning Protocol (RPP) data objects, as defined in [@!I-D.kowalik-rpp-data-objects], using the JavaScript Object Notation (JSON) Data Interchange Format [@!RFC8259]. It specifies how RPP primitive types, common data types, component objects, resource objects, and associations are mapped to JSON and JSON Schema, and provides normative JSON Schema definitions and worked examples for domain name, contact, and host data objects.

{mainmatter}

# Introduction

The RESTful Provisioning Protocol (RPP) defines a set of data objects for managing foundational registry resources including domain names, contacts, and hosts. The data model is defined in [@!I-D.kowalik-rpp-data-objects] independently of any particular representation format. This document defines the JSON [@!RFC8259] representation of those data objects.

JSON has emerged as the de facto standard data format for modern RESTful APIs. Its widespread adoption across tools, libraries, and developer communities makes it well suited as the primary representation format for RPP. This document provides the normative rules and JSON Schema definitions required for implementations to produce and consume RPP messages in JSON.

The separation between the abstract data model and its concrete JSON representation ensures that the protocol's semantic foundation remains stable while enabling the adoption of JSON across diverse deployment environments.

## Motivation

The RESTful Provisioning Protocol (RPP) introduces a new provisioning mechanism that aligns more closely with modern cloud infrastructure, enhancing the scalability of server deployments. While RESTful protocols do not mandate a specific media type for resource description, the widespread adoption of JSON in web services has established it as the de facto standard for modern APIs. The increasing availability of tools, software libraries, and a skilled workforce has led several registries to adopt JSON for data exchange within their API ecosystems. Registries supporting JSON can offer a unified API ecosystem that extends beyond domain name and IP address provisioning, maintaining a consistent technology stack, data formats, and developer experience.

JSON's syntax, known for its straightforwardness and minimal verbosity, significantly eases the tasks of writing, reading, and maintaining code. This simplicity is especially advantageous for the rapid comprehension and integration of provisioning APIs.

The lightweight nature of JSON can result in faster processing and data transfers, a critical aspect in high-volume transaction environments such as domain registration. Enhanced API response times can lead to more efficient domain lookups, registrations, and updates. JSON parsing is typically fast and well-supported by standard libraries, contributing to improved system performance amid frequent interactions between RPP clients and servers.

However, the absence of a standardised JSON format for domain provisioning has led to the emergence of TLD-specific implementations that lack interoperability, increasing the development effort required for integration. Similarly, at the registrar level, the absence of standards has resulted in numerous incompatible API implementations provided to clients and resellers. Standardising a JSON format for domain provisioning within the RPP framework could mitigate these challenges, reducing fragmentation and simplifying integration efforts across the domain registration industry.

# Terminology

In this document the following terminology is used.

RPP Data Objects - The abstract data model definitions for domain name, contact, and host resources, as specified in [@!I-D.kowalik-rpp-data-objects].

RESTful Provisioning Protocol - A RESTful protocol for provisioning heterogeneous database objects.

JSON Schema - A vocabulary that allows annotation and validation of JSON documents, as described in [@?JSON-SCHEMA].

EPP Compatibility Profile - A set of additional constraints defined in [@!I-D.kowalik-rpp-data-objects] that a server MUST adhere to when supporting both RPP and EPP concurrently.

# Conventions Used in This Document

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in [@!RFC2119].

JSON is case sensitive. Unless stated otherwise, JSON specifications and examples provided in this document MUST be interpreted in the character case presented. The examples in this document assume that request and response messages are properly formatted JSON documents. Indentation and white space in examples are provided only to illustrate element relationships and for improving readability, and are not REQUIRED features of the protocol.

All JSON Schema definitions in this document use JSON Schema draft 2020-12 [@?JSON-SCHEMA], and where not provided with a `$schema` keyword, the following default applies:

```json
"$schema": "https://json-schema.org/draft/2020-12/schema"
```

# JSON Representation Rules

This section defines the normative rules for representing the RPP data model in JSON. The data model is specified in [@!I-D.kowalik-rpp-data-objects], which defines all primitive types, common data types, component objects, resource objects, and associations independently of any concrete representation format. The rules in this section specify how those abstract definitions map to JSON and JSON Schema version 2020-12.

## Primitive Type Mappings

RPP primitive types MUST be represented in JSON as follows:

| RPP Primitive Type | JSON Type   | Notes                                                                          |
|--------------------|-------------|--------------------------------------------------------------------------------|
| String             | `string`    | Unicode character sequence                                                     |
| Integer            | `integer`   | Whole number, positive or negative                                             |
| Boolean            | `boolean`   | `true` or `false`                                                              |
| Decimal            | `number`    | Base-10 fractional value                                                       |
| Date               | `string`    | Full-date as per [@!RFC3339], e.g. `"2025-10-27"`                             |
| Timestamp          | `string`    | Date-time in UTC as per [@!RFC3339], e.g. `"2025-10-27T09:42:51Z"`           |
| URL                | `string`    | Uniform Resource Locator as per [@!RFC1738]                                    |
| Binary             | `string`    | Base64-encoded binary data                                                     |

Example Timestamp:

```json
"creationDate": "1999-04-03T22:00:00.0Z"
```

Example Date:

```json
"expiryDate": "2025-10-27"
```

## Common Data Type Mappings

This section defines shared data types that are based on the primitive data types above and are re-used across multiple data object definitions. Each common data type maps to a JSON Schema definition.

### Identifier

Identifiers are character strings with a specified minimum length, a specified maximum length, and a specified format outlined in [@!RFC5730, section 2.8]. Identifiers for certain object types MAY have additional constraints imposed either by server policy, object-specific specifications, or both.

<!-- TODO: Add required identifiers -->

### Client Identifier

Client identifiers are character strings with a specified minimum length, a specified maximum length, and a specified format. Client identifiers use the `clIDType` syntax described in [@!RFC5730].

In JSON, a Client Identifier MUST be represented as a `string` value.

```json
{
  "$defs": {
    "clientIdentifier": {
      "type": "string",
      "minLength": 3,
      "maxLength": 16,
      "pattern": "^[a-zA-Z0-9]([-a-zA-Z0-9]*[a-zA-Z0-9])?$"
    }
  }
}
```

### Phone Number

Telephone number syntax is derived from structures defined in [@!ITU.E164.2005]. Telephone numbers described in this specification are character strings that MUST begin with a plus sign ("+", ASCII value 0x002B), followed by a country code defined in [@!ITU.E164.2005], followed by a dot (".", ASCII value 0x002E), followed by a sequence of digits representing the telephone number. An optional "x" (ASCII value 0x0078) separator with additional digits representing extension information can be appended to the end of the value.

In JSON, a Phone Number MUST be represented as a `string` value conforming to the pattern described above.

```json
{
  "$defs": {
    "phoneNumber": {
      "type": "string",
      "pattern": "^\\+[0-9]{1,3}\\.[0-9]+( x[0-9]+)?$"
    }
  }
}
```

Example Phone Number values:

```json
"voice": "+1.7035555555",
"mobile": "+1.7035555556"
```

## Cardinality Rules

The cardinality of each data element in the RPP data model MUST be represented as follows in JSON:

Rule 1: A data element with cardinality `1` (exactly one) MUST be represented as a JSON property and MUST be present in the containing JSON object. The element MUST be listed under `required` in the corresponding JSON Schema.

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" }
  },
  "required": ["name"]
}
```

Rule 2: A data element with cardinality `0-1` (zero or one) MUST be represented as an optional JSON property. The element MUST NOT be listed under `required` in the corresponding JSON Schema. When absent, the element MUST be omitted from the JSON object (not represented as `null`).

```json
{
  "type": "object",
  "properties": {
    "expiryDate": { "type": "string", "format": "date-time" }
  }
}
```

Rule 3: A data element with cardinality `0+` (zero or more) MUST be represented as an optional JSON array. When no values are present, the property MUST be omitted or represented as an empty array.

```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "array",
      "items": { "$ref": "#/$defs/status" }
    }
  }
}
```

Rule 4: A data element with cardinality `1+` (one or more) MUST be represented as a required JSON array with `"minItems": 1` and the element MUST be listed under `required` in the corresponding JSON Schema.

```json
{
  "type": "object",
  "properties": {
    "postalInfo": {
      "type": "array",
      "items": { "$ref": "#/$defs/postalInfo" },
      "minItems": 1
    }
  },
  "required": ["postalInfo"]
}
```

## Mutability Rules

Data elements in the RPP data model carry a mutability attribute: `create-only`, `read-only`, or `read-write`. These MUST be represented in JSON Schema as follows:

Rule 5: Data elements with mutability `read-only` MUST be annotated with `"readOnly": true` in the JSON Schema. Clients MUST NOT include read-only properties in create or update request bodies. Servers MUST ignore any read-only properties provided by a client in a request.

```json
{
  "repositoryId": {
    "type": "string",
    "readOnly": true
  }
}
```

Rule 6: Data elements with mutability `create-only` MUST be annotated with `"writeOnly": true` in the JSON Schema for request schemas, and excluded from update request schemas. Servers MUST reject requests that attempt to modify a `create-only` element after object creation.

Rule 7: Data elements with mutability `read-write` have no additional annotation. They MAY appear in both request and response bodies.

## Association Rules

The RPP data model defines several association types between objects, the following rules specify their JSON representations.
A Aggregation represents a relationship between two independent objects, where one object references another. A Composition represents a parent-child relationship where the child object is embedded within the parent object and cannot exist independently.

### Aggregation

An `Aggregation[Type]` represents a relationship between two independent objects. When the cardinality allows more than one target, it MUST be represented as a JSON array. Each element of the array MUST be the identifier of the referenced object.

Rule 8: `Aggregation[Type]` with cardinality `0+` or `1+` MUST be represented as a JSON array of embedded objects. Each object in the array MUST include the data elements of the referenced object type that are relevant to the context (at minimum the primary identifier field). Other data elements of the referenced object type MAY be included as needed to provide additional context for the client, but are not required. The JSON Schema MUST allow for the presence of these additional fields.

Example: domain nameservers (Aggregation[Host Data Object]) in a read response, returning a limited object representation, only cvontaining the primary identifier field `hostName`:

```json
{
    "@type": "domainName",
    "name": "name.example",
    "nameservers": [
        { "@type": "host", "hostName": "ns1.name.example" },
        { "@type": "host", "hostName": "ns2.name.example" }
    ]
}
```

### Composition

A `Composition[Type]` represents a parent-child relationship where the child's lifecycle is bound to the parent and the child cannot exist independently of the parent. In JSON, the child object MUST be fully embedded within the parent object. The JSON representation of a composition is the same as that of an aggregation. The distinction between the two is semantic and does not affect the JSON structure.

```json
{ 
        "@type": "domainName",
        "name": "name.example",
        "nameservers": [
            {
                "@type": "host",
                "hostName": "ns1.name.example",
                "provisioningMetadata": {
                    "@type": "provisioningMetadata",
                    "repositoryId": "NS1EXAMPLE-REP",
                    "sponsoringClientId": "ClientX"
                },
                "status": [ { "@type": "status", "label": "ok" } ],
                "dns": [
                    {
                        "@type": "dnsResourceRecord",
                        "hostNamelabel": "ns1.name.example",
                        "type": "A",
                        "data": "192.0.2.1",
                        "ttl": 3600
                    }
                ]
            }
        ]
}
```

### Labelled Aggregation

A `LabelledAggregation[Type]` is a relationship between two independent objects where each association carries a string label. Multiple associations with the same label are allowed.

Rule 9: `LabelledAggregation[Type]` with cardinality `0+` MUST be represented as a JSON array of objects. Each object in the array MUST contain a `label` property (string) alongside the identifier of the referenced object. The object MUST include at least the primary identifier field of the referenced object type. Other data elements of the referenced object type MAY be included as needed to provide additional context for the client, but are not required. The JSON Schema MUST allow for the presence of these additional fields.

Example: domain contacts (LabelledAggregation[Contact Object]):

```json
"contacts": [
    { 
        "label": "admin",
        "object": { 
            "@type": "contact",
            "id": "ABC-8013" 
        }
    },
    { 
        "label": "tech",
        "object": { 
            "@type": "contact",
            "id": "ABC-8014" 
        }
     }
]
```

### Dictionary Aggregation

A `DictionaryAggregation[Type]` is a relationship between two independent objects where each association carries a unique string label that serves as a dictionary key.

Rule 10: `DictionaryAggregation[Type]` MUST be represented as a JSON object where each key is the unique label and the corresponding value is the referenced object, the object MUST include at least the primary identifier field of the referenced object type. Other data elements of the referenced object type MAY be included as needed to provide additional context for the client, but are not required. The JSON Schema MUST allow for the presence of these additional fields.

Example: domain contacts keyed by unique role (DictionaryAggregation[Contact Object]):

```json
"contacts": {
    "admin": {
        "@type": "contact",
        "id": "ABC-8013"
    },
    "tech": {
        "@type": "contact",
        "id": "ABC-8014"
    }
}
```

### Labelled Composition

A `LabelledComposition[Type]` is a parent-child relationship where each embedded child carries a string label. Multiple instances with the same label are allowed.

Rule 11: `LabelledComposition[Type]` with cardinality `0+` MUST be represented as a JSON array of embedded objects. Each object in the array MUST contain a `label` property alongside the data elements of the composed type.

Example: contact postal info (LabelledComposition[Postal Info Object]):

```json
"addresses": [
    {
        "label": "int",
        "postalInfo": {
            "@type": "postalInfo",
            "type": "PERSON",
            "name": "John Doe",
            "addr": {
                "@type": "postalAddress",
                "street": ["123 Example Dr."],
                "city": "Dulles",
                "sp": "VA",
                "pc": "20166-6503",
                "cc": "US"
            }
        }
    }
]
```

### Dictionary Composition

A `DictionaryComposition[Type]` is a parent-child relationship where each embedded child carries a unique string label used as a dictionary key.

Rule 12: `DictionaryComposition[Type]` MUST be represented as a JSON object where each key is the unique label and the corresponding value is the fully embedded child object.

Example: contact postal info (DictionaryComposition[Postal Info Object]):

```json
"addresses": {
    "int": {
        "@type": "postalInfo",
        "type": "PERSON",
        "name": "John Doe",
        "addr": {
            "@type": "postalAddress",
            "street": ["123 Example Dr."],
            "city": "Dulles",
            "sp": "VA",
            "pc": "20166-6503",
            "cc": "US"
        }
    }
}
```

## Object Identifier Rules

Rule 13: When a resource or component object is referenced by identifier (for example in an aggregation), the identifier MUST be represented as a JSON string using the value of the object's primary identifier data element.

Rule 14: When a resource or component object is embedded (as in a composition), all data elements of the object MUST be represented as properties of a JSON object according to the rules of this section.

## JSON Schema Definition Rules

Rule 15: Each RPP component object and resource object MUST have a corresponding JSON Schema definition. Object definitions MUST be placed in the `$defs` keyword of the JSON Schema document.

Rule 16: Identifier fields MUST use `"type": "string"` in JSON Schema.

Rule 17: Enumeration constraints on string fields MUST be expressed using the `"enum"` keyword in JSON Schema.

Example (Transfer Status enum):

```json
"transferStatus": {
    "type": "string",
    "enum": ["pending", "clientApproved", "clientCancelled",
             "clientRejected", "serverApproved", "serverCancelled"]
}
```

Rule 18: Each JSON Schema definition for an RPP object MUST include a `"required"` array listing all data elements with cardinality `1` or `1+`.

Rule 19: JSON Schema definitions for RPP objects MUST use `"additionalProperties": false` by default to prevent unrecognised properties.

Rule 20: Every RPP object representation MUST include a `"@type"` property whose value is the object's identifier as registered in the IANA RPP Data Object Registry. This property enables JSON-LD type identification and allows clients and servers to unambiguously determine the type of an object. The `"@type"` property MUST be included in the JSON Schema `"properties"` object for each RPP object definition with a `"const"` constraint fixing the value to the object's registered identifier. The `"@type"` property MUST be listed in the `"required"` array of the corresponding JSON Schema definition.

Example (Domain Name Data Object):

```json
{
  "@type": "domainName",
  "name": "example.com"
}
```

The following table lists all RPP objects and their corresponding `@type` values:

| Object Name                      | `@type` Value              |
|----------------------------------|----------------------------|
| Domain Name Data Object          | `domainName`               |
| Contact Data Object              | `contact`                  |
| Host Data Object                 | `host`                     |
| Provisioning Metadata Object     | `provisioningMetadata`     |
| Status Object                    | `status`                   |
| Period Object                    | `period`                   |
| DNS Resource Record              | `dnsResourceRecord`        |
| Authorisation Information Object | `authorisationInformation` |
| Transfer Data Object             | `transferData`             |
| Postal Info Object               | `postalInfo`               |
| Postal Address Object            | `postalAddress`            |

# JSON Schema Definitions

This section provides normative JSON Schema definitions for RPP component objects and resource objects. All schemas use JSON Schema draft 2020-12 [@?JSON-SCHEMA].

<!-- TODO: can we say normative for json schema definitions? -->

## Common Component Schemas

### Period Object

```json
{
  "$defs": {
    "period": {
      "type": "object",
      "properties": {
        "@type": { "type": "string", "const": "period" },
        "value": {
          "type": "integer",
          "minimum": 1,
          "maximum": 99
        },
        "unit": {
          "type": "string",
          "enum": ["y", "m"]
        }
      },
      "required": ["@type", "value", "unit"],
      "additionalProperties": false
    }
  }
}
```

### Provisioning Metadata Object

```json
{
  "$defs": {
    "provisioningMetadata": {
      "type": "object",
      "properties": {
        "@type":              { "type": "string", "const": "provisioningMetadata", "readOnly": true },
        "repositoryId":       { "type": "string", "readOnly": true },
        "sponsoringClientId": { "type": "string", "readOnly": true },
        "creatingClientId":   { "type": "string", "readOnly": true },
        "creationDate":       { "type": "string", "format": "date-time", "readOnly": true },
        "updatingClientId":   { "type": "string", "readOnly": true },
        "updateDate":         { "type": "string", "format": "date-time", "readOnly": true },
        "transferDate":       { "type": "string", "format": "date-time", "readOnly": true }
      },
      "required": ["@type", "sponsoringClientId"],
      "additionalProperties": false
    }
  }
}
```

### Status Object

```json
{
  "$defs": {
    "status": {
      "type": "object",
      "properties": {
        "@type":  { "type": "string", "const": "status" },
        "label":  { "type": "string" },
        "reason": { "type": "string" },
        "due":    { "type": "string", "format": "date-time" }
      },
      "required": ["@type", "label"],
      "additionalProperties": false
    }
  }
}
```

### DNS Resource Record

```json
{
  "$defs": {
    "dnsResourceRecord": {
      "type": "object",
      "properties": {
        "@type":         { "type": "string", "const": "dnsResourceRecord" },
        "hostNamelabel": { "type": "string" },
        "type":          { "type": "string" },
        "data":          { "type": "string" },
        "ttl":           { "type": "integer" }
      },
      "required": ["@type", "hostNamelabel", "type", "data", "ttl"],
      "additionalProperties": false
    }
  }
}
```

### Authorisation Information Object

```json
{
  "$defs": {
    "authorisationInformation": {
      "type": "object",
      "properties": {
        "@type":    { "type": "string", "const": "authorisationInformation" },
        "method":   { "type": "string" },
        "authdata": { "type": "string" }
      },
      "required": ["@type", "method", "authdata"],
      "additionalProperties": false
    }
  }
}
```

### Postal Address Object

```json
{
  "$defs": {
    "postalAddress": {
      "type": "object",
      "properties": {
        "@type": { "type": "string", "const": "postalAddress" },
        "street": {
          "type": "array",
          "items": { "type": "string" }
        },
        "city":  { "type": "string" },
        "sp":    { "type": "string" },
        "pc":    { "type": "string" },
        "cc":    { "type": "string", "minLength": 2, "maxLength": 2 }
      },
      "required": ["@type"],
      "additionalProperties": false
    }
  }
}
```

### Postal Info Object

```json
{
  "$defs": {
    "postalInfo": {
      "type": "object",
      "properties": {
        "@type": { "type": "string", "const": "postalInfo" },
        "type": {
          "type": "string",
          "enum": ["PERSON", "ORG"]
        },
        "name": { "type": "string" },
        "org":  { "type": "string" },
        "addr": { "$ref": "#/$defs/postalAddress" }
      },
      "required": ["@type"],
      "additionalProperties": false
    }
  }
}
```

### Transfer Data Object

```json
{
  "$defs": {
    "transferData": {
      "type": "object",
      "properties": {
        "@type": { "type": "string", "const": "transferData", "readOnly": true },
        "transferStatus": {
          "type": "string",
          "enum": ["pending", "clientApproved", "clientCancelled",
                   "clientRejected", "serverApproved", "serverCancelled"],
          "readOnly": true
        },
        "transferDirection": {
          "type": "string",
          "enum": ["pull", "push"],
          "readOnly": true
        },
        "requestingClientId": { "type": "string", "readOnly": true },
        "requestDate":        { "type": "string", "format": "date-time", "readOnly": true },
        "actingClientId":     { "type": "string", "readOnly": true },
        "actionDate":         { "type": "string", "format": "date-time", "readOnly": true }
      },
      "required": [
        "@type", "transferStatus", "transferDirection", "requestingClientId",
        "requestDate", "actingClientId", "actionDate"
      ],
      "additionalProperties": false
    }
  }
}
```

## Resource Object Schemas

### Domain Name Data Object

The Domain Name Data Object represents a domain name and its associated provisioning data.

Create request schema (create-only and read-write properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "@type": { "type": "string", "const": "domainName" },
    "name": { "type": "string" },
    "registrant": { "type": "string" },
    "contacts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "label": { "type": "string" },
          "id":    { "type": "string" }
        },
        "required": ["label", "id"],
        "additionalProperties": false
      }
    },
    "nameservers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "@type":   { "type": "string", "const": "host" },
          "hostName": { "type": "string" },
          "dns": {
            "type": "array",
            "items": { "$ref": "#/$defs/dnsResourceRecord" }
          }
        },
        "required": ["@type", "hostName"],
        "additionalProperties": false
      }
    },
    "dns": {
      "type": "array",
      "items": { "$ref": "#/$defs/dnsResourceRecord" }
    },
    "authorisationInformation": { "$ref": "#/$defs/authInfo" },
    "period":   { "$ref": "#/$defs/period" }
  },
  "required": ["@type", "name"],
  "additionalProperties": false,
  "$defs": {
    "dnsResourceRecord": {
      "type": "object",
      "properties": {
        "@type":         { "type": "string", "const": "dnsResourceRecord" },
        "hostNamelabel": { "type": "string" },
        "type":          { "type": "string" },
        "data":          { "type": "string" },
        "ttl":           { "type": "integer" }
      },
      "required": ["@type", "hostNamelabel", "type", "data", "ttl"],
      "additionalProperties": false
    },
    "authorisationInformation": {
      "type": "object",
      "properties": {
        "@type":    { "type": "string", "const": "authorisationInformation" },
        "method":   { "type": "string" },
        "authdata": { "type": "string" }
      },
      "required": ["@type", "method", "authdata"],
      "additionalProperties": false
    },
    "period": {
      "type": "object",
      "properties": {
        "@type": { "type": "string", "const": "period" },
        "value": { "type": "integer", "minimum": 1, "maximum": 99 },
        "unit":  { "type": "string", "enum": ["y", "m"] }
      },
      "required": ["@type", "value", "unit"],
      "additionalProperties": false
    }
  }
}
```

Read response schema (read-write and read-only properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "@type":                 { "type": "string", "const": "domainName", "readOnly": true },
    "name":                  { "type": "string", "readOnly": true },
    "provisioningMetadata":  { "$ref": "#/$defs/provisioningMetadata" },
    "status": {
      "type": "array",
      "items": { "$ref": "#/$defs/status" },
      "readOnly": true
    },
    "registrant":  { "type": "string" },
    "contacts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "label": { "type": "string" },
          "id":    { "type": "string" }
        },
        "required": ["label", "id"],
        "additionalProperties": false
      }
    },
    "nameservers": {
      "type": "array",
      "items": { "$ref": "#/$defs/host" }
    },
    "dns": {
      "type": "array",
      "items": { "$ref": "#/$defs/dnsResourceRecord" }
    },
    "subordinateHosts": {
      "type": "array",
      "items": { "$ref": "#/$defs/host" },
      "readOnly": true
    },
    "expiryDate": { "type": "string", "format": "date-time", "readOnly": true },
    "authorisationInformation":   { "$ref": "#/$defs/authInfo" }
  },
  "required": ["@type", "name", "provisioningMetadata"],
  "additionalProperties": false,
  "$defs": {
    "host": {
      "type": "object",
      "properties": {
        "@type":              { "type": "string", "const": "host", "readOnly": true },
        "hostName":            { "type": "string" },
        "provisioningMetadata": { "$ref": "#/$defs/provisioningMetadata" },
        "status": {
          "type": "array",
          "items": { "$ref": "#/$defs/status" },
          "readOnly": true
        },
        "dns": {
          "type": "array",
          "items": { "$ref": "#/$defs/dnsResourceRecord" }
        }
      },
      "required": ["@type", "hostName"],
      "additionalProperties": false
    }
  }
}
```

### Contact Data Object

Create request schema (create-only and read-write properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "@type": { "type": "string", "const": "contact" },
    "id": { "type": "string" },
    "postalInfo": {
      "type": "object",
      "additionalProperties": { "$ref": "#/$defs/postalInfo" },
      "minProperties": 1
    },
    "voice": {
      "type": "array",
      "items": { "type": "string" }
    },
    "fax": {
      "type": "array",
      "items": { "type": "string" }
    },
    "email": {
      "type": "array",
      "items": { "type": "string", "format": "email" }
    },
    "authorisationInformation": { "$ref": "#/$defs/authInfo" },
    "disclose":  { "type": "object" }
  },
  "required": ["@type", "id", "postalInfo"],
  "additionalProperties": false
}
```

Read response schema (read-write and read-only properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "@type":                 { "type": "string", "const": "contact", "readOnly": true },
    "id": { "type": "string", "readOnly": true },
    "provisioningMetadata": { "$ref": "#/$defs/provisioningMetadata" },
    "status": {
      "type": "array",
      "items": { "$ref": "#/$defs/status" },
      "readOnly": true
    },
    "postalInfo": {
      "type": "object",
      "additionalProperties": { "$ref": "#/$defs/postalInfo" },
      "minProperties": 1
    },
    "voice": {
      "type": "array",
      "items": { "type": "string" }
    },
    "fax": {
      "type": "array",
      "items": { "type": "string" }
    },
    "email": {
      "type": "array",
      "items": { "type": "string", "format": "email" }
    },
    "authorisationInformation": { "$ref": "#/$defs/authInfo" },
    "disclose":  { "type": "object" }
  },
  "required": ["@type", "id", "provisioningMetadata", "postalInfo"],
  "additionalProperties": false
}
```

### Host Data Object

Create request schema (create-only and read-write properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "@type":    { "type": "string", "const": "host" },
    "hostName": { "type": "string" },
    "dns": {
      "type": "array",
      "items": { "$ref": "#/$defs/dnsResourceRecord" }
    }
  },
  "required": ["@type", "hostName"],
  "additionalProperties": false
}
```

Read response schema (read-write and read-only properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "@type":    { "type": "string", "const": "host", "readOnly": true },
    "hostName": { "type": "string" },
    "provisioningMetadata": { "$ref": "#/$defs/provisioningMetadata" },
    "status": {
      "type": "array",
      "items": { "$ref": "#/$defs/status" },
      "readOnly": true
    },
    "dns": {
      "type": "array",
      "items": { "$ref": "#/$defs/dnsResourceRecord" }
    }
  },
  "required": ["@type", "hostName", "provisioningMetadata"],
  "additionalProperties": false
}
```

# Examples

This section provides examples that follow the JSON representation rules and JSON Schema definitions specified in the previous sections. The examples illustrate typical request and response messages for domain name, contact, and host resources.

## Domain Name

### Create

Example domain create request:

```json
{
    "@type": "domainName",
    "name": "example.com",
    "period": {
        "@type": "period",
        "value": 2,
        "unit": "y"
    },
    "nameservers": [
        { "@type": "host", "hostName": "ns1.example.net" },
        { "@type": "host", "hostName": "ns2.example.net" }
    ],
    "registrant": "jd1234",
    "contacts": [
        { "label": "admin", "id": "sh8013" },
        { "label": "tech",  "id": "sh8013" }
    ],
    "authorisationInformation": {
        "@type": "authorisationInformation",
        "method": "authinfo",
        "authdata": "2fooBAR"
    }
}
```

Example domain create response:

```json
{
    "@type": "domainName",
    "name": "example.com",
    "provisioningMetadata": {
        "@type": "provisioningMetadata",
        "repositoryId": "EXAMPLE1-REP",
        "sponsoringClientId": "ClientX",
        "creatingClientId": "ClientX",
        "creationDate": "1999-04-03T22:00:00.0Z"
    },
    "expiryDate": "2001-04-03T22:00:00.0Z"
}
```

### Read

Example domain read response:

```json
{
    "@type": "domainName",
    "name": "example.com",
    "provisioningMetadata": {
        "@type": "provisioningMetadata",
        "repositoryId": "EXAMPLE1-REP",
        "sponsoringClientId": "ClientX",
        "creatingClientId": "ClientY",
        "creationDate": "1999-04-03T22:00:00.0Z",
        "updatingClientId": "ClientX",
        "updateDate": "1999-12-03T09:00:00.0Z",
        "transferDate": "2000-04-08T09:00:00.0Z"
    },
    "status": [
        { "@type": "status", "label": "ok" }
    ],
    "registrant": "jd1234",
    "contacts": [
        { "label": "admin", "id": "sh8013" },
        { "label": "tech",  "id": "sh8013" }
    ],
    "nameservers": [
        {
            "@type": "host",
            "hostName": "ns1.example.com",
            "provisioningMetadata": {
                "@type": "provisioningMetadata",
                "repositoryId": "NS1EXAMPLE-REP",
                "sponsoringClientId": "ClientX"
            },
            "status": [ { "@type": "status", "label": "ok" } ],
            "dns": [
                {
                    "@type": "dnsResourceRecord",
                    "hostNamelabel": "ns1.example.com.",
                    "type": "A",
                    "data": "192.0.2.1",
                    "ttl": 3600
                }
            ]
        },
        {
            "@type": "host",
            "hostName": "ns1.example.net",
            "provisioningMetadata": {
                "@type": "provisioningMetadata",
                "repositoryId": "NS1EXAMPLENET-REP",
                "sponsoringClientId": "ClientZ"
            },
            "status": [ { "@type": "status", "label": "ok" } ]
        }
    ],
    "subordinateHosts": [
        {
            "@type": "host",
            "hostName": "ns1.example.com",
            "provisioningMetadata": {
                "@type": "provisioningMetadata",
                "repositoryId": "NS1EXAMPLE-REP",
                "sponsoringClientId": "ClientX"
            },
            "status": [ { "@type": "status", "label": "ok" } ]
        },
        {
            "@type": "host",
            "hostName": "ns2.example.com",
            "provisioningMetadata": {
                "@type": "provisioningMetadata",
                "repositoryId": "NS2EXAMPLE-REP",
                "sponsoringClientId": "ClientX"
            },
            "status": [ { "@type": "status", "label": "ok" } ]
        }
    ],
    "expiryDate": "2005-04-03T22:00:00.0Z",
    "authorisationInformation": {
        "@type": "authorisationInformation",
        "method": "authinfo",
        "authdata": "2fooBAR"
    }
}
```

### Update

Example domain update request (read-write properties):

```json
{
    "@type": "domainName",
    "registrant": "sh8013",
    "authorisationInformation": {
        "@type": "authorisationInformation",
        "method": "authinfo",
        "authdata": "2BARfoo"
    }
}
```

Example domain update response:

```json
{
    "@type": "domainName",
    "name": "example.com",
    "provisioningMetadata": {
        "@type": "provisioningMetadata",
        "repositoryId": "EXAMPLE1-REP",
        "sponsoringClientId": "ClientX",
        "creatingClientId": "ClientY",
        "creationDate": "1999-04-03T22:00:00.0Z",
        "updatingClientId": "ClientX",
        "updateDate": "2000-01-15T09:00:00.0Z"
    },
    "status": [
        { "@type": "status", "label": "ok" }
    ],
    "registrant": "sh8013"
}
```

### Delete

The domain delete operation takes the domain name as the resource identifier in the request. No request body is required.

Example domain delete response (minimal, server may return full representation):

```json
{
    "@type": "domainName",
    "name": "example.com",
    "provisioningMetadata": {
        "@type": "provisioningMetadata",
        "repositoryId": "EXAMPLE1-REP",
        "sponsoringClientId": "ClientX"
    }
}
```

### Renew

The renew operation accepts a transient `currentExpiryDate` parameter for validation and an optional `renewalPeriod`.

Example domain renew request:

```json
{
    "currentExpiryDate": "2005-04-03T22:00:00.0Z",
    "renewalPeriod": {
        "@type": "period",
        "value": 5,
        "unit": "y"
    }
}
```

Example domain renew response:

```json
{
    "@type": "domainName",
    "name": "example.com",
    "expiryDate": "2010-04-03T22:00:00.0Z"
}
```

### Transfer Request

Example domain transfer request (pull transfer):

```json
{
    "transferDirection": "pull",
    "authorisationInformation": {
        "@type": "authorisationInformation",
        "method": "authinfo",
        "authdata": "2fooBAR"
    },
    "transferPeriod": {
        "@type": "period",
        "value": 1,
        "unit": "y"
    }
}
```

Example domain transfer response (Transfer Data Object):

```json
{
    "@type": "transferData",
    "transferStatus": "pending",
    "transferDirection": "pull",
    "requestingClientId": "ClientX",
    "requestDate": "2000-06-08T22:00:00.0Z",
    "actingClientId": "ClientY",
    "actionDate": "2000-06-13T22:00:00.0Z",
    "expiryDate": "2002-09-08T22:00:00.0Z"
}
```

### Transfer Query

Example domain transfer query response (Transfer Data Object):

```json
{
    "@type": "transferData",
    "transferStatus": "pending",
    "transferDirection": "pull",
    "requestingClientId": "ClientX",
    "requestDate": "2000-06-06T22:00:00.0Z",
    "actingClientId": "ClientY",
    "actionDate": "2000-06-11T22:00:00.0Z",
    "expiryDate": "2002-09-08T22:00:00.0Z"
}
```

### Transfer Cancel / Reject / Approve

Transfer cancel, reject, and approve responses return the Transfer Data Object. The response structure is the same as the Transfer Query response above. The `transferStatus` value reflects the outcome of the operation (e.g. `"clientCancelled"`, `"clientRejected"`, or `"clientApproved"`).

## Contact

### Create

Example contact create request:

```json
{
    "@type": "contact",
    "id": "jd1234",
    "postalInfo": {
        "int": {
            "@type": "postalInfo",
            "type": "PERSON",
            "name": "John Doe",
            "org": "Example Inc.",
            "addr": {
                "@type": "postalAddress",
                "street": [
                    "123 Example Dr.",
                    "Suite 100"
                ],
                "city": "Dulles",
                "sp": "VA",
                "pc": "20166-6503",
                "cc": "US"
            }
        }
    },
    "voice": ["+1.7035555555"],
    "fax": ["+1.7035555556"],
    "email": ["jdoe@example.com"],
    "authorisationInformation": {
        "@type": "authorisationInformation",
        "method": "authinfo",
        "authdata": "2fooBAR"
    }
}
```

Example contact create response:

```json
{
    "@type": "contact",
    "id": "jd1234",
    "provisioningMetadata": {
        "@type": "provisioningMetadata",
        "repositoryId": "JD1234-REP",
        "sponsoringClientId": "ClientX",
        "creatingClientId": "ClientX",
        "creationDate": "1999-04-03T22:00:00.0Z"
    },
    "status": [
        { "@type": "status", "label": "ok" }
    ],
    "postalInfo": {
        "int": {
            "@type": "postalInfo",
            "type": "PERSON",
            "name": "John Doe",
            "org": "Example Inc.",
            "addr": {
                "@type": "postalAddress",
                "street": [
                    "123 Example Dr.",
                    "Suite 100"
                ],
                "city": "Dulles",
                "sp": "VA",
                "pc": "20166-6503",
                "cc": "US"
            }
        }
    },
    "voice": ["+1.7035555555"],
    "fax": ["+1.7035555556"],
    "email": ["jdoe@example.com"]
}
```

### Read

Example contact read response:

```json
{
    "@type": "contact",
    "id": "jd1234",
    "provisioningMetadata": {
        "@type": "provisioningMetadata",
        "repositoryId": "JD1234-REP",
        "sponsoringClientId": "ClientX",
        "creatingClientId": "ClientX",
        "creationDate": "1999-04-03T22:00:00.0Z",
        "updatingClientId": "ClientX",
        "updateDate": "2000-01-15T09:00:00.0Z"
    },
    "status": [
        { "@type": "status", "label": "ok" }
    ],
    "postalInfo": {
        "int": {
            "@type": "postalInfo",
            "type": "PERSON",
            "name": "John Doe",
            "org": "Example Inc.",
            "addr": {
                "@type": "postalAddress",
                "street": ["123 Example Dr.", "Suite 100"],
                "city": "Dulles",
                "sp": "VA",
                "pc": "20166-6503",
                "cc": "US"
            }
        }
    },
    "voice": ["+1.7035555555"],
    "email": ["jdoe@example.com"]
}
```

## Host

### Create

Example host create request:

```json
{
    "@type": "host",
    "hostName": "ns1.example.com",
    "dns": [
        {
            "@type": "dnsResourceRecord",
            "hostNamelabel": "ns1.example.com.",
            "type": "A",
            "data": "192.0.2.1",
            "ttl": 3600
        },
        {
            "@type": "dnsResourceRecord",
            "hostNamelabel": "ns1.example.com.",
            "type": "AAAA",
            "data": "2001:db8::1",
            "ttl": 3600
        }
    ]
}
```

Example host create response:

```json
{
    "@type": "host",
    "hostName": "ns1.example.com",
    "provisioningMetadata": {
        "@type": "provisioningMetadata",
        "repositoryId": "NS1EXAMPLE-REP",
        "sponsoringClientId": "ClientX",
        "creatingClientId": "ClientX",
        "creationDate": "1999-04-03T22:00:00.0Z"
    },
    "status": [
        { "@type": "status", "label": "ok" }
    ],
    "dns": [
        {
            "@type": "dnsResourceRecord",
            "hostNamelabel": "ns1.example.com.",
            "type": "A",
            "data": "192.0.2.1",
            "ttl": 3600
        },
        {
            "@type": "dnsResourceRecord",
            "hostNamelabel": "ns1.example.com.",
            "type": "AAAA",
            "data": "2001:db8::1",
            "ttl": 3600
        }
    ]
}
```

### Read

Example host read response:

```json
{
    "@type": "host",
    "hostName": "ns1.example.com",
    "provisioningMetadata": {
        "@type": "provisioningMetadata",
        "repositoryId": "NS1EXAMPLE-REP",
        "sponsoringClientId": "ClientX",
        "creatingClientId": "ClientY",
        "creationDate": "1999-04-03T22:00:00.0Z"
    },
    "status": [
        { "@type": "status", "label": "ok" }
    ],
    "dns": [
        {
            "@type": "dnsResourceRecord",
            "hostNamelabel": "ns1.example.com.",
            "type": "A",
            "data": "192.0.2.1",
            "ttl": 3600
        }
    ]
}
```

### Update

Example host update request:

```json
{
    "@type": "host",
    "hostName": "ns1.example2.com",
    "dns": [
        {
            "@type": "dnsResourceRecord",
            "hostNamelabel": "ns1.example2.com.",
            "type": "A",
            "data": "198.51.100.1",
            "ttl": 3600
        }
    ]
}
```

### Delete

The host delete operation takes the host name as the resource identifier. No request body is required. The server SHOULD reject the request if the host object is associated with any domain name objects.

# IANA Considerations

TODO

# Internationalization Considerations

TODO

# Security Considerations

TODO

# Acknowledgments

TODO

{backmatter}

<reference anchor="JSON-SCHEMA" target="https://json-schema.org/draft/2020-12/json-schema-core">
  <front>
    <title>JSON Schema: A Media Type for Describing JSON Documents</title>
    <author>
      <organization>JSON Schema</organization>
    </author>
    <date year="2020"/>
  </front>
</reference>

<reference anchor="ITU.E164.2005">
  <front>
    <title>The international public telecommunication numbering plan</title>
    <author>
      <organization>International Telecommunication Union</organization>
    </author>
    <date year="2005" month="02"/>
  </front>
  <seriesInfo name="ITU-T Recommendation" value="E.164"/>
</reference>
