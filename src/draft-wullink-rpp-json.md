%%%
title = "JSON for Restful Provisioning Protocol (RPP)"
abbrev = "JSON for RPP"
ipr = "trust200902"
area = "Internet"
workgroup = "Network Working Group"
submissiontype = "IETF"
keyword = [""]
TocDepth = 4

[seriesInfo]
name = "Internet-Draft"
value = "draft-wullink-rpp-json-02"
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

```
  "$schema": "https://json-schema.org/draft/2020-12/schema"
```

# JSON Representation Rules

This section defines the normative rules for representing the RPP data model in JSON. The data model is specified in [@!I-D.kowalik-rpp-data-objects], which defines all primitive types, common data types, component objects, resource objects, and associations independently of any concrete representation format. The rules in this section specify how those abstract definitions map to JSON and JSON Schema version 2020-12.

## Primitive Type Mappings

RPP primitive types MUST be represented in JSON as follows:

| RPP Primitive Type | JSON Type   | Notes                                                                          |
|--------------------|-------------|--------------------------------------------------------------------------------|
| String             | `string`    | Unicode character sequence                                                     |
| Integer            | `number`    | Whole number, positive or negative                                             |
| Boolean            | `boolean`   | `true` or `false`                                                              |
| Decimal            | `string`    | Base-10 fractional value with exact representation within a defined precision. Number is encoded into string same as `"number"` in [@!RFC8259] without exponent part `"ext"`. |
| Date               | `string`    | Full-date as per [@!RFC3339], e.g. `"2025-10-27"`                              |
| Timestamp          | `string`    | Date-time in UTC as per [@!RFC3339], e.g. `"2025-10-27T09:42:51Z"`             |
| URL                | `string`    | Uniform Resource Locator as per [@!RFC1738]                                    |
| Binary             | `string`    | Base64-encoded binary data                                                     |

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
    "records": {
      "type": "array",
      "items": { "$ref": "#/$defs/dnsRecord" },
      "minItems": 1
    }
  },
  "required": ["records"]
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

### Labelled associations

Some associations between objects carry a string label that provides additional context for the relationship. The label is not an identifier of the target object, but rather a descriptor of the association itself. Labelled associations can occur in both aggregations and compositions. When representing labelled associations in JSON, the property `label` MUST be included  alongside the reference to the target object. A property with the name `object` MUST be used to contain the reference to the target object, which can be either limited representation containing at minimum the primary object identifier for aggregations or an embedded object for compositions.

<!-- TODO: update text to clarify what data objects attribute must be used for unique object identifier in aggregation examples -->

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
                "provMetadata": {
                    "@type": "provMetadata",
                    "repositoryId": "NS1EXAMPLE-REP",
                    "spClientId": "ClientX"
                },
                "status": [ { "@type": "status", "label": "ok" } ],
                "dns": {
                    "@type": "dnsData",
                    "records": [
                        {
                            "@type": "dnsRecord",
                            "name": "@",
                            "type": "ns",
                            "rdata": { "nsdname": "ns1.name.example." }
                        },
                        {
                            "@type": "dnsRecord",
                            "name": "ns1.name.example.",
                            "type": "a",
                            "rdata": { "address": "192.0.2.1" }
                        }
                    ]
                }
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

Example: remarks (LabelledComposition[Remark Object]):

```json
"remarks": [
    {
        "label": "public",
        "object": {
            "@type": "remark",
            "description": "This domain is used for test purposes."
        }
    },
    {
        "label": "private",
        "object": {
            "@type": "remark",
            "description": "Internal note for the sponsoring client."
        }
    }
]
```

### Dictionary Composition

A `DictionaryComposition[Type]` is a parent-child relationship where each embedded child carries a unique string label used as a dictionary key.

Rule 12: `DictionaryComposition[Type]` MUST be represented as a JSON object where each key is the unique label and the corresponding value is the fully embedded child object.

Example: remarks keyed by scope (DictionaryComposition[Remark Object]):

```json
"remarks": {
    "public": {
        "@type": "remark",
        "description": "This domain is used for test purposes."
    },
    "private": {
        "@type": "remark",
        "description": "Internal note for the sponsoring client."
    }
}
```

## Object Identifier Rules

Rule 13: When a resource or component object is referenced by identifier (for example in an aggregation), the identifier MUST be represented as a JSON string using the value of the object's primary identifier data element.

Rule 14: When a resource or component object is embedded (as in a composition), all data elements of the object MUST be represented as properties of a JSON object according to the rules of this section.

## External Type Embedding Rules

RPP data objects may include data elements whose types are defined by external specifications (e.g., JSContact in [@!RFC9553]). When embedding a value of an externally defined type into a JSON representation, the following rules apply, in order of preference:

Rule 15: If the external type has a native JSON representation (i.e., the external specification defines how the type is represented using the JSON format), the value MUST be embedded as a valid JSON element using the native JSON representation defined by that specification.

Rule 16: If the external type does not have a native JSON representation but has a native UTF-8 encoded text representation, the value MUST be embedded as a JSON `string` using the UTF-8 encoding.

Rule 17: If the external type has neither a native JSON nor a native UTF-8 text representation, the binary representation of the value MUST be Base64-encoded ([@!RFC4648], Section 4) and embedded as a JSON `string`.

## Process Data Embedding Rules

As defined in [@!I-D.wullink-rpp-core], a uniform interface operation MAY require process data in addition to the object representation data. This section defines how such process data MUST be represented in JSON when transmitted together with the object representation in a single request body.

Rule 18: Process data accompanying a uniform interface operation MUST be represented using the `processes` data element of the owning resource object (see Processes Object), following the Aggregation rules for the corresponding process type (for example `createProcess` for creation-specific inputs). Each embedded process object MUST be a valid JSON representation of the process object. This applies uniformly regardless of whether the resource object already exists.

Example: a domain create request body carrying a two-year registration period as process data embedded in a `createProcess` process object under `processes`:

```json
{
    "@type": "domainName",
    "name": "example.example",
    "nameservers": [
        { "@type": "host", "hostName": "ns1.example.example" },
        { "@type": "host", "hostName": "ns2.example.example" }
    ],
    "processes": {
        "@type": "processes",
        "createProcess": [
            {
                "@type": "createProcess",
                "period": {
                    "@type": "period",
                    "value": 2,
                    "unit": "y"
                }
            }
        ]
    }
}
```

## JSON Schema Definition Rules

Rule 20: Each RPP component object and resource object MUST have a corresponding JSON Schema definition. Object definitions MUST be placed in the `$defs` keyword of the JSON Schema document.

Rule 21: Identifier fields MUST use `"type": "string"` in JSON Schema.

Rule 22: Enumeration constraints on string fields MUST be expressed using the `"enum"` keyword in JSON Schema.

Example (Transfer Status enum):

```json
"trStatus": {
    "type": "string",
    "enum": ["pending", "clientApproved", "clientCancelled",
             "clientRejected", "serverApproved", "serverCancelled"]
}
```

Rule 23: Each JSON Schema definition for an RPP object MUST include a `"required"` array listing all data elements with cardinality `1` or `1+`.


Rule 24: JSON Schema definitions for extendible RPP objects MUST NOT use `"additionalProperties": false` or `"unevaluatedProperties": false`. However, before validation, schemas on every property level MUST be enriched with `"unevaluatedProperties": false` property to prevent the presence of undeclared properties in JSON instances. JSON Schemas for Object type MAY use `"additionalProperties": true` to allow for free key definition.

<!-- Implementation of this is a nightmare, because one as to take care to put unevaluatedProperties: false on top level of allOf/anyOf branches, but not in the branches themselves. See inject_unevaluated_properties() function in the verification script. -->

Rule 25: Every RPP object representation MUST include a `"@type"` property whose value is the object's identifier as registered in the IANA RPP Data Object Registry. This property enables identification and allows clients and servers to unambiguously determine the type of an object. The `"@type"` property MUST be included in the JSON Schema `"properties"` object for each RPP object definition with a `"const"` constraint fixing the value to the object's registered identifier. The `"@type"` property MUST be listed in the `"required"` array of the corresponding JSON Schema definition.

Example (Domain Name Data Object):

```json
{
    "@type": "domainName",
    "name": "example.example"
}
```

Rule 26: When a transfer request or other operation requires authorization information (e.g., EPP-style authinfo), the client MUST NOT include the `authInfo` object in the JSON request body. Instead, the client MUST convey the authorization information using the `RPP-Authorization` HTTP request header as defined in [@!I-D.wullink-rpp-core]. Servers MUST reject any request that includes an `authInfo` object in the JSON body with an appropriate error response.

### RPP Profiles and Validation

RPP profiles, such as the EPP Compatibility Profile defined in [@!I-D.kowalik-rpp-data-objects], may impose additional constraints on top of the base RPP data model. These additional constraints MUST be enforced by implementations through validation rules that go beyond what can be expressed in JSON Schema. Such validation rules MUST be clearly documented in the profile specification and implemented by both clients and servers when operating under that profile. For example, the EPP Compatibility Profile requires that certain fields be present in specific object types, and that certain identifier fields conform to EPP syntax rules. These constraints cannot be fully captured in JSON Schema and therefore require additional validation logic in implementations.

# JSON Schema Definitions

This section provides normative JSON Schema definitions for RPP component objects and resource objects. All schemas use JSON Schema draft 2020-12 [@?JSON-SCHEMA].

<!-- TODO: can we say normative for json schema definitions? -->

## Common Data Types Schemas

This section defines shared data types that are based on the primitive data types above and are re-used across multiple data object definitions. 

### Identifier

Identifiers are character strings with a specified minimum length, a specified maximum length, and a specified format outlined in [@!RFC5730, section 2.8]. Identifiers for certain object types MAY have additional constraints imposed either by server policy, object-specific specifications, or both.

In JSON, an Identifier MUST be represented as a `string` value conforming to the `roidType` syntax defined in [@!RFC5730, section 2.8]: one to eight word characters optionally preceded by an underscore, followed by a hyphen and one or more word characters, with a maximum total length of 89 characters.

```json
{
  "$defs": {
    "identifier": {
      "type": "string",
      "pattern": "^(\\w|_){1,8}-\\w{1,}$",
      "maxLength": 89
    }
  }
}
```

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

## Component Objects Schemas

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
      "required": ["@type", "value", "unit"]
    }
  }
}
```

### Provisioning Metadata Object

The following constraints cannot be expressed in JSON Schema and MUST be enforced by implementations:

- `upClientId` and `upDate` MUST NOT be present if the object has never been modified.
- `trDate` MUST NOT be present if the object has never been transferred.
- In EPP Compatibility Profile, `repositoryId` MUST be provided.

```json
{
  "$defs": {
    "provMetadata": {
      "type": "object",
      "properties": {
        "@type":       { "type": "string", "const": "provMetadata", "readOnly": true },
        "repositoryId": { "type": "string", "readOnly": true },
        "spClientId":  { "$ref": "#/$defs/clientIdentifier", "readOnly": true },
        "crClientId":  { "$ref": "#/$defs/clientIdentifier", "readOnly": true },
        "crDate":      { "type": "string", "format": "date-time", "readOnly": true },
        "upClientId":  { "$ref": "#/$defs/clientIdentifier", "readOnly": true },
        "upDate":      { "type": "string", "format": "date-time", "readOnly": true },
        "trDate":      { "type": "string", "format": "date-time", "readOnly": true }
      },
      "required": ["@type", "spClientId"]
    }
  }
}
```

### Status Object

The following constraints cannot be expressed in JSON Schema and MUST be enforced by implementations:

- `label` MUST use camelCase notation using only ASCII alphabetic characters. Labels set explicitly by the server MUST use the prefix "server"; labels set explicitly by a client MUST use the prefix "client"; all other labels MUST NOT use either prefix. The allowed set of label values depends on the provisioning object type and MAY be extended by extensions.
- `due`: Servers MAY restrict the ability of clients to set or update this value.
- When the RGP feature is supported, the following additional status labels MAY appear on objects that support RGP: `addPeriod`, `autoRenewPeriod`, `renewPeriod`, `transferPeriod`, `redemptionPeriod`, `pendingRestore`, `rgpPendingDelete`. The labels `redemptionPeriod`, `pendingRestore`, and `rgpPendingDelete` MUST only appear alongside the standard `pendingDelete` status.

```json
{
  "$defs": {
    "status": {
      "type": "object",
      "properties": {
        "@type":  { "type": "string", "const": "status" },
        "label":  { "type": "string", "pattern": "^[a-zA-Z]+$" },
        "reason": { "type": "string" },
        "due":    { "type": "string", "format": "date-time" }
      },
      "required": ["@type", "label"]
    }
  }
}
```

### DNS Resource Record Object

The following constraints cannot be expressed in JSON Schema and MUST be enforced by implementations:

- `name` MUST be a syntactically valid DNS host name in zone file string representation. Both absolute FQDNs (with trailing dot) and relative host names are allowed, as well as the `@` symbol representing the domain name itself.
- `type` MUST be a valid string representation of a DNS resource record type as defined in [@!RFC1035]. Values MUST be converted to lower case. Allowed values MAY be further constrained by server policy.
- In EPP Compatibility Profile ([@!RFC5732]), the following record types MUST be supported: `ns`, `a`, and `aaaa`. With DNSSEC Extension [@RFC5910], `ds` and `dnskey` MUST additionally be supported.
- `class`, if present, MUST be chosen from Section 3.2.4 (CLASS values) of [@!RFC1035]. A client SHOULD omit this element; the server MUST assume `IN` as the default.
- The fields within `rdata` MUST match the expected structure for the given record type (see RDATA structures below).

RDATA structures required in EPP Compatibility Profile:

- NS records ([@!RFC1035], Section 3.3.11): `nsdname`
- A records ([@!RFC1035], Section 3.4.1): `address`
- AAAA records ([@RFC3596], Section 2.2): `address`
- DS records ([@RFC4034], Section 5, with DNSSEC Extension): `keyTag`, `algorithm`, `digestType`, `digest`
- DNSKEY records ([@RFC4034], Section 2, with DNSSEC Extension): `flags`, `protocol`, `algorithm`, `publicKey`

All `rdata` property names MUST be written in camelCase and all values MUST use the string data type.

```json
{
  "$defs": {
    "dnsRecord": {
      "type": "object",
      "properties": {
        "@type": { "type": "string", "const": "dnsRecord" },
        "name":  { "type": "string" },
        "class": { "type": "string" },
        "type":  { "type": "string" },
        "rdata": { "type": "object", "unevaluatedProperties": true }
      },
      "required": ["@type", "name", "type", "rdata"]
    }
  }
}
```

### DNS Operational Controls Object

The DNS Operational Controls Object contains operational control parameters that a client MAY use to influence server-side DNS behaviour for a set of DNS records. A server MAY ignore these values, e.g. for policy reasons. This structure is aligned with [@I-D.simmen-rpp-dns-data].

```json
{
  "$defs": {
    "dnsControls": {
      "type": "object",
      "properties": {
        "@type": { "type": "string", "const": "dnsControls" },
        "ttl": {
          "type": "object",
            "propertyNames": {
              "pattern": "^[a-z]+$"
            },
          "additionalProperties": { "type": "integer", "minimum": 1 }
        },
        "maxSigLifetime": {
          "type": "object",
          "propertyNames": {
            "pattern": "^[a-z]+$"
          },
          "additionalProperties": { "type": "integer", "minimum": 1 }
        }
      },
      "required": ["@type"]
    }
  }
}
```

### DNS Data Object

The DNS Data Object is a container for DNS resource records and associated operational controls for a provisioned object. This structure groups DNS records together with control parameters that influence server-side DNS behaviour. It is aligned with [@I-D.simmen-rpp-dns-data].

The following constraints cannot be expressed in JSON Schema and MUST be enforced by implementations:

- In EPP Compatibility Profile with DNSSEC Extension [@RFC5910], records of type `ds` and `dnskey` MUST be supported in addition to `ns`, `a`, and `aaaa`. A server MUST support either `ds` or `dnskey` or both. If provided with only `dnskey`, a server MUST calculate the DS record.

```json
{
  "$defs": {
    "dnsData": {
      "type": "object",
      "properties": {
        "@type": { "type": "string", "const": "dnsData" },
        "records": {
          "type": "array",
          "items": { "$ref": "#/$defs/dnsRecord" }
        },
        "controls": { "$ref": "#/$defs/dnsControls" }
      },
      "required": ["@type"]
    }
  }
}
```

### Authorisation Information Object

The following constraints cannot be expressed in JSON Schema and MUST be enforced by implementations:

- `method` MUST be one of the values registered in the IANA RPP Authorisation Method Registry as defined in [@!I-D.wullink-rpp-core]. In EPP Compatibility Profile, this value MUST be "authinfo" for standard password-based authorisation.
- The Authorisation Information Object is immutable. When authorisation information changes, a new instance MUST be created rather than modifying the existing one. The value of `authdata` MAY not be returned in read responses, depending on the method and server policy.

```json
{
  "$defs": {
    "authInfo": {
      "type": "object",
      "properties": {
        "@type":    { "type": "string", "const": "authInfo" },
        "method":   { "type": "string" },
        "authdata": { "type": "string" }
      },
      "required": ["@type", "method", "authdata"]
    }
  }
}
```

### JSContact Card Object

The Contact Data Object uses version 2.0 of JSContact [@!RFC9982] to represent contact information. The `Contact` object is defined below according to the RPP JSContact Profile [TODO Add Ref].

The following constraints cannot be expressed in JSON Schema and MUST be enforced by implementations:

- `addresses[*].countryCode` MUST be a valid two-character ISO 3166-1 [@!ISO3166-1] alpha-2 code when present.
- `localizations` MUST be fully expanded; nested PatchObject-style keys (e.g., `"addresses/addr/full"`) are NOT allowed.
- When `phones[*].features` is absent, the number MUST be treated as a voice number.

```json
{
  "$defs": {
    "Card": {
      "type": "object",
      "properties": {
        "@type":    { "type": "string", "const": "Card" },
        "version":  { "type": "string", "const": "2.0" },
        "kind":     { "type": "string", "enum": ["individual", "org"] },
        "language": { "type": "string" },
        "name": {
          "type": "object",
          "properties": {
            "full": { "type": "string" },
            "components": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "kind":  { "type": "string", "enum": ["given", "surname"] },
                  "value": { "type": "string" }
                },
                "required": ["kind", "value"]
              }
            }
          }
        },
        "organizations": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "name": { "type": "string" }
            }
          }
        },
        "addresses": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "full":        { "type": "string" },
              "countryCode": { "type": "string", "pattern": "^[A-Z]{2}$" },
              "components": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "kind":  { "type": "string", "enum": ["name", "locality", "region", "postcode", "country"] },
                    "value": { "type": "string" }
                  },
                  "required": ["kind", "value"]
                }
              }
            }
          }
        },
        "phones": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "number":   { "type": "string" },
              "features": {
                "type": "object",
                "additionalProperties": {
                  "type": "boolean"
                }
              }
            },
            "required": ["number"]
          }
        },
        "emails": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "address": { "type": "string", "format": "email" }
            },
            "required": ["address"]
          }
        },
        "links": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "uri":  { "type": "string", "format": "uri" },
              "kind": { "type": "string", "const": "contact" }
            },
            "required": ["uri"]
          }
        },
        "localizations": { "type": "object" }
      },
      "required": ["@type", "version"]
    }
  }
}
```

### Restore Report Object

The Restore Report Object contains the redemption grace period restore report submitted by the sponsoring client as required by the RGP process ([@!RFC3915]).

The following constraints cannot be expressed in JSON Schema and MUST be enforced by implementations:

* At least one and at most two `statements` MUST be provided.
* `restoreTime` MAY be omitted when the restore report is submitted inline within the restore request in a single-step process.
* In EPP Compatibility Profile, `restoreTime` MUST be present as defined in [@!RFC3915].
* In EPP Compatibility Profile, exactly two `statements` MUST be present as defined in [@!RFC3915].

```json
{
  "$defs": {
    "restoreReport": {
      "type": "object",
      "properties": {
        "@type":         { "type": "string", "const": "restoreReport" },
        "preData":       { "type": "string" },
        "postData":      { "type": "string" },
        "deleteTime":    { "type": "string", "format": "date-time" },
        "restoreTime":   { "type": "string", "format": "date-time" },
        "restoreReason": { "type": "string" },
        "statements": {
          "type": "array",
          "items": { "type": "string" },
          "minItems": 1,
          "maxItems": 2
        },
        "other": { "type": "string" }
      },
      "required": ["@type", "statements"]
    }
  }
}
```

### Organisation Role Object

The following constraints cannot be expressed in JSON Schema and MUST be enforced by implementations:

- `type` MUST only use values registered in the IANA "EPP Organization Role Values" registry ([@!RFC8543]).

```json
{
  "$defs": {
    "organisationRole": {
      "type": "object",
      "properties": {
        "@type":  { "type": "string", "const": "organisationRole" },
        "status": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["ok", "linked", "clientLinkProhibited", "serverLinkProhibited"]
          }
        },
        "roleId": { "type": "string" }
      },
      "required": ["@type"]
    }
  }
}
```

### Processes Object

The Processes Object is a read-only container grouping the currently active Process Objects on the owning resource object, keyed by process type. Each key holds an array of the corresponding Process Object's read representation, per the Aggregation rules.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/processes",
  "$defs": {
    "processes": {
      "type": "object",
      "properties": {
        "@type":           { "type": "string", "const": "processes", "readOnly": true },
        "createProcess":   {
          "type": "array",
          "items": { "$ref": "#/$defs/createProcess.read" },
          "readOnly": true
        },
        "renewProcess":    {
          "type": "array",
          "items": { "$ref": "#/$defs/renewProcess.read" },
          "readOnly": true
        },
        "transferProcess": {
          "type": "array",
          "items": { "$ref": "#/$defs/transferProcess.read" },
          "readOnly": true
        },
        "restoreProcess":  {
          "type": "array",
          "items": { "$ref": "#/$defs/restoreProcess.read" },
          "readOnly": true
        }
      },
      "required": ["@type"]
    }
  }
}
```

## Process Object Schemas

### Create Process Object

The Create Process Object carries the process-specific inputs for a resource creation operation, such as the requested registration period. It is submitted as an element of the `createProcess` array under the `processes` data element of the owning resource object (see Processes Object), following the same Aggregation representation as the other process types.

Create request schema (create-only and read-write properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/createProcess.create",
  "$defs": {
    "createProcess.create": {
      "type": "object",
      "properties": {
        "@type": { "type": "string", "const": "createProcess" },
        "period": { "$ref": "#/$defs/period" }
      },
      "required": ["@type"]
    }
  }
}
```

Read response schema (read-only properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/createProcess.read",
  "$defs": {
    "createProcess.read": {
      "type": "object",
      "properties": {
        "@type":  { "type": "string", "const": "createProcess", "readOnly": true },
        "period": { "$ref": "#/$defs/period", "readOnly": true }
      },
      "required": ["@type"]
    }
  }
}
```

### Renew Process Object

Renew request schema (create-only properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/renewProcess.create",
  "$defs": {
    "renewProcess.create": {
      "type": "object",
      "properties": {
        "@type":         { "type": "string", "const": "renewProcess" },
        "expiryDate":    { "type": "string", "format": "date-time" },
        "renewalPeriod": { "$ref": "#/$defs/period" }
      },
      "required": ["@type"]
    }
  }
}
```

Renew response schema (read-only properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/renewProcess.read",
  "$defs": {
    "renewProcess.read": {
      "type": "object",
      "properties": {
        "@type":      { "type": "string", "const": "renewProcess", "readOnly": true },
        "expiryDate": { "type": "string", "format": "date-time", "readOnly": true }
      },
      "required": ["@type"]
    }
  }
}
```

### Transfer Process Object

#### Create

Create request schema (create-only and read-write properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/transferProcess.create",
  "$defs": {
    "transferProcess.create": {
      "type": "object",
      "oneOf": [
        {
          "properties": {
            "@type": { "type": "string", "const": "transferProcess"},
            "transferDir": {
              "type": "string",
              "const": "push"
            },
            "gainingClientId": { "$ref": "#/$defs/clientIdentifier" }
          },
          "required": [
            "@type", "transferDir", "gainingClientId"
          ]
        },
        {
          "properties": {
            "@type": { "type": "string", "const": "transferProcess" },
            "transferDir": {
              "type": "string",
              "const": "pull"
            }
          },
          "required": [
            "@type", "transferDir"
          ]
        }
      ]
    }
  }
}
```

#### Read

Read response schema (read-write and read-only properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/transferProcess.read",
  "$defs": {
    "transferProcess.read": {
      "type": "object",
      "properties": {
        "@type": { "type": "string", "const": "transferProcess", "readOnly": true },
        "trStatus": {
          "type": "string",
          "enum": ["pending", "clientApproved", "clientCancelled",
                    "clientRejected", "serverApproved", "serverCancelled"],
          "readOnly": true
        },
        "transferDir": {
          "type": "string",
          "enum": ["pull", "push"],
          "readOnly": true
        },
        "gainingClientId": { "$ref": "#/$defs/clientIdentifier", "readOnly": true },
        "reqClientId": { "$ref": "#/$defs/clientIdentifier", "readOnly": true},
        "requestDate": { "type": "string", "format": "date-time", "readOnly": true },
        "actClientId": { "$ref": "#/$defs/clientIdentifier", "readOnly": true },
        "actionDate":  { "type": "string", "format": "date-time", "readOnly": true }
      },
      "required": [
        "@type", "transferDir", "trStatus", "reqClientId",
        "requestDate", "actClientId", "actionDate"
      ]
    }
  }
}
```

#### Approve

The Approve operation MUST always have a request body, which may be an empty JSON object. The server can identify the transfer process to be approved based on the request URL and the authenticated client's permissions. There is no Approve request schema defined in this specification.

The Approve response schema MUST equal the read response schema.

#### Cancel

The Cancel operation, which is similar to a delete operation, has no request body, the server can identify the transfer process to be cancelled based on the request URL and the authenticated client's permissions. Because the Cancel operation has no request body, it is not possible to extend the request schema with additional properties.

The Cancel response schema MUST equal the read response schema or an empty response.

#### Reject

Reject request schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/transferProcess.reject",
  "$defs": {
    "transferProcess.reject": {
      "type": "object",
      "properties": {
        "@type":  { "type": "string", "const": "transferProcess" },
        "reason": { "type": "string" }
      },
      "required": ["@type"]
    }
  }
}
```

Reject response schema MUST equal the read response schema.

### Restore Process Object

The Restore Process Object represents the current state of a restore request for an object that has entered the Redemption Grace Period (RGP). It is returned as a response for all restore operations.

The following constraints cannot be expressed in JSON Schema and MUST be enforced by implementations:

* `requestDate` MUST NOT be present if no restore request has been submitted yet.
* `reportDate` MUST NOT be present if no restore report has been accepted yet.
* `reportDueDate` MUST NOT be present when `restoreStatus` is not `"pendingRestore"`.

Create request schema (create-only and read-write properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/restoreProcess.create",
  "$defs": {
    "restoreProcess.create": {
      "type": "object",
      "properties": {
        "@type":         { "type": "string", "const": "restoreProcess" },
        "restoreReport": { "$ref": "#/$defs/restoreReport" }
      },
      "required": ["@type"]
    }
  }
}
```

Read response schema (read-write and read-only properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/restoreProcess.read",
  "$defs": {
    "restoreProcess.read": {
      "type": "object",
      "properties": {
        "@type":         { "type": "string", "const": "restoreProcess", "readOnly": true },
        "restoreStatus": {
          "type": "string",
          "enum": ["pendingRestore", "restored", "rgpPendingDelete"],
          "readOnly": true
        },
        "requestDate":   { "type": "string", "format": "date-time", "readOnly": true },
        "reportDate":    { "type": "string", "format": "date-time", "readOnly": true },
        "reportDueDate": { "type": "string", "format": "date-time", "readOnly": true }
      },
      "required": ["@type", "restoreStatus"]
    }
  }
}
```


## Domain Name Data Object

The Domain Name Data Object represents a domain name and its associated provisioning data.

The following constraints cannot be expressed in JSON Schema and MUST be enforced by implementations:

- `name` MUST be a fully qualified domain name conforming to the syntax described in [@!RFC1035]. Servers MAY restrict allowable domain names to a specific namespace for which they are authoritative. The implicit trailing dot MUST NOT be included.

### Create

Create request schema (create-only and read-write properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/domainObject.create",
  "$defs": {
    "domainObject.create": {
      "type": "object",
      "properties": {
        "@type": { "type": "string", "const": "domainName" },
        "name": { "type": "string", "writeOnly": true },
        "registrant": { "$ref": "#/$defs/contactObject.reference" },
        "contacts": {
          "type": "array",
          "items": { 
            "type": "object",
            "properties": {
              "label": { "type": "string" },
              "object": { "$ref": "#/$defs/contactObject.reference" }
            },
            "required": ["label", "object"]
           }
        },
        "nameservers": {
          "type": "array",
          "items": { "$ref": "#/$defs/hostObject.reference" }
        },
        "dns":    { "$ref": "#/$defs/dnsData" },
        "authInfo": { "$ref": "#/$defs/authInfo" },
        "processes": {
          "type": "object",
          "properties": {
            "@type": { "type": "string", "const": "processes" },
            "createProcess": {
              "type": "array",
              "items": { "$ref": "#/$defs/createProcess.create" },
              "maxItems": 1
            }
          },
          "required": ["@type"]
        }
      },
      "required": ["@type", "name"]
    }
  }
}
```

### Read

Read response schema (read-write and read-only properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/domainObject.read",
  "$defs": {
    "domainObject.read": {
      "type": "object",
      "properties": {
        "@type":       { "type": "string", "const": "domainName", "readOnly": true },
        "name":        { "type": "string", "readOnly": true },
        "provMetadata": { "$ref": "#/$defs/provMetadata" },
        "status": {
          "type": "array",
          "items": { "$ref": "#/$defs/status" },
          "readOnly": true
        },
        "registrant":  { "$ref": "#/$defs/contactObject.reference" },
        "contacts": {
          "type": "array",
          "items": { 
            "type": "object",
            "properties": {
              "label": { "type": "string" },
              "object": { "$ref": "#/$defs/contactObject.reference" }
            },
            "required": ["label", "object"]
           }
        },
        "nameservers": {
          "type": "array",
          "items": { "$ref": "#/$defs/hostObject.reference" }
        },
        "dns":    { "$ref": "#/$defs/dnsData" },
        "subordinateHosts": {
          "type": "array",
          "items": { "$ref": "#/$defs/hostObject.reference" },
          "readOnly": true
        },
        "expiryDate": { "type": "string", "format": "date-time", "readOnly": true },
        "authInfo":  { "$ref": "#/$defs/authInfo" },
        "processes": { "$ref": "#/$defs/processes", "readOnly": true }
      },
      "required": ["@type", "name", "provMetadata"]
    }
  }
}
```

### Update

Update request schema (read-write properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/domainObject.update",
  "$defs": {
    "domainObject.update": {
      "type": "object",
      "properties": {
        "@type": { "type": "string", "const": "domainName" },
        "registrant": { "$ref": "#/$defs/contactObject.reference" },
        "contacts": {
          "type": "array",
          "items": { 
            "type": "object",
            "properties": {
              "label": { "type": "string" },
              "object": { "$ref": "#/$defs/contactObject.reference" }
            },
            "required": ["label", "object"]
           }
        },
        "nameservers": {
          "type": "array",
          "items": { "$ref": "#/$defs/hostObject.reference" }
        },
        "dns":    { "$ref": "#/$defs/dnsData" },
        "authInfo": { "$ref": "#/$defs/authInfo" }
      },
      "required": ["@type"]
    }
  }
}
```

### Renew

Renew minimal response schema (only expire date):


```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/renewProcess.create.domain",
  "$defs": {
    "renewProcess.create.domain": {
       "$ref": "#/$defs/renewProcess.create"
    }
  }
}
```

### Transfer

Create request for Domain Transfer Process Object schema (create-only and read-write properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/transferProcess.create.domain",
  "$defs": {
    "transferProcess.create.domain": {
      "allOf": [
        { "$ref": "#/$defs/transferProcess.create" },
        {
          "properties": {
            "transferPeriod": { "$ref": "#/$defs/period" }
          }
        }
      ]
    }
  }
}
```

Read response for Domain Transfer Process Object schema (read-write and read-only properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/transferProcess.read.domain",
  "$defs": {
    "transferProcess.read.domain": {
      "allOf": [
        { "$ref": "#/$defs/transferProcess.read" },
        {
          "properties": {
            "expiryDate":  { "type": "string", "format": "date-time", "readOnly": true }
          }
        }
      ]
    }
  }
}
```

Both Approve and Delete (Cancel) operations have no request body, the server can identify the transfer process to be approved or cancelled based on the request URL and the authenticated client's permissions.

Delete (Cancel) response Domain Transfer Process Object schema (read-write and read-only properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/transferProcess.delete.domain",
  "$defs": {
    "transferProcess.delete.domain": {
      "$ref": "#/$defs/transferProcess.read.domain"
    }
  }
}
```

Approve response Domain Transfer Process Object schema (read-write and read-only properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/transferProcess.approve.domain",
  "$defs": {
    "transferProcess.approve.domain": {
      "$ref": "#/$defs/transferProcess.read.domain"
    }
  }
}
```

Reject request Domain Object schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/transferProcess.reject.domain",
  "$defs": {
    "transferProcess.reject.domain": {
      "$ref": "#/$defs/transferProcess.reject"
    }
  }
}
```

Reject response schema (read-write and read-only properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/transferProcess.reject.domain",
  "$defs": {
    "transferProcess.reject.domain": {
      "$ref": "#/$defs/transferProcess.read.domain"
    }
  }
}
```

### Reference

Reference schema (identifier only):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/domainObject.reference",
  "$defs": {
    "domainObject.reference": {
      "type": "object",
      "properties": {
        "@type":       { "type": "string", "const": "domainName", "readOnly": true },
        "name":        { "type": "string", "readOnly": true }
      },
      "required": ["@type", "name"]
    }
  }
}
```

## Contact Data Object

This document uses version 2.0 of JSContact [@!RFC9982] for the JSON representation of Contact Data Object contact information. The contact's name, postal address, phone numbers, email addresses, and other contact details are encapsulated in a JSContact `Card` object embedded in the `contactInfo` property.

### JSContact Profile for RPP

Since JSContact is a general-purpose representation of contact data, this document defines a restricted usage profile for use within RPP, see [TODO: ref to RPP JSContact profile here: https://github.com/SIDN/ietf-rpp-jscontact-profile].

The following constraints cannot be expressed in JSON Schema and MUST be enforced by implementations:

- `card.name.full` MUST be provided in EPP Compatibility Profile.
- `card.addresses.addr` MUST be provided in EPP Compatibility Profile, containing at least `countryCode` and a `"locality"` kind component.
- `card.emails.email.address` MUST be provided in EPP Compatibility Profile.
- `card.addresses[*].countryCode` MUST be a valid two-character ISO 3166-1 [@!ISO3166-1] alpha-2 code when present.

### Create

Create request schema (create-only and read-write properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/contactObject.create",
  "$defs": {
    "contactObject.create": {
      "type": "object",
      "properties": {
        "@type":  { "type": "string", "const": "contact" },
        "id":     { "type": "string" },
        "contactInfo":   { "$ref": "#/$defs/Card" },
        "authInfo": { "$ref": "#/$defs/authInfo" }
      },
      "required": ["@type", "id", "contactInfo"],
      "unevaluatedProperties": false
    }
  }
}
```

### Read

Read response schema (read-write and read-only properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/contactObject.read",
  "$defs": {
    "contactObject.read": {
      "type": "object",
      "properties": {
        "@type":  { "type": "string", "const": "contact", "readOnly": true },
        "id":     { "type": "string", "readOnly": true },
        "provMetadata": { "$ref": "#/$defs/provMetadata" },
        "status": {
          "type": "array",
          "items": { "$ref": "#/$defs/status" },
          "readOnly": true
        },
        "contactInfo":   { "$ref": "#/$defs/Card" },
        "authInfo": { "$ref": "#/$defs/authInfo" }
      },
      "required": ["@type", "id", "provMetadata", "contactInfo"],
      "unevaluatedProperties": false
    }
  }
}
```

### Update

Update request schema (read-write properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/contactObject.update",
  "$defs": {
    "contactObject.update": {
      "type": "object",
      "properties": {
        "@type":  { "type": "string", "const": "contact" },
        "contactInfo":   { "$ref": "#/$defs/Card" },
        "authInfo": { "$ref": "#/$defs/authInfo" },
        "processes": { "$ref": "#/$defs/processes", "readOnly": true }
      },
      "required": ["@type", "contactInfo"],
      "unevaluatedProperties": false
    }
  }
}
```

### Transfer

Transfer create request for Contact Object schema (create-only and read-write properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/transferProcess.create.contact",
  "$defs": {
    "transferProcess.create.contact": {
      "$ref": "#/$defs/transferProcess.create"
    }
  }
}
```

### Reference 

Reference schema (identifier only):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/contactObject.reference",
  "$defs": {
    "contactObject.reference": {
      "type": "object",
      "properties": {
        "@type":         { "type": "string", "const": "contact", "readOnly": true },
        "id":            { "type": "string", "readOnly": true }
      },
      "required": ["@type", "id"]
    }
  }
}
```

## Host Data Object

The following constraints cannot be expressed in JSON Schema and MUST be enforced by implementations:

- `hostName` MUST be a syntactically valid fully qualified host name.
- If the host name is subordinate to a domain for which the server is authoritative, the superordinate domain MUST already exist in the server.

### Create

Create request schema (create-only and read-write properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/hostObject.create",
  "$defs": {
    "hostObject.create": {
      "type": "object",
      "properties": {
        "@type":    { "type": "string", "const": "host" },
        "hostName": { "type": "string", "format": "hostname" },
        "dns":      { "$ref": "#/$defs/dnsData" }
      },
      "required": ["@type", "hostName"]
    }
  }
}
```

### Read

Read response schema (read-write and read-only properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/hostObject.read",
  "$defs": {
    "hostObject.read": {
      "type": "object",
      "properties": {
        "@type":         { "type": "string", "const": "host", "readOnly": true },
        "hostName":      { "type": "string", "format": "hostname" },
        "provMetadata":  { "$ref": "#/$defs/provMetadata" },
        "status": {
          "type": "array",
          "items": { "$ref": "#/$defs/status" },
          "readOnly": true
        },
        "dns":           { "$ref": "#/$defs/dnsData" },
        "processes":     { "$ref": "#/$defs/processes", "readOnly": true }
      },
      "required": ["@type", "hostName", "provMetadata"]
    }
  }
}
```

### Update

TODO

### Reference

Reference schema (identifier only):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/hostObject.reference",
  "$defs": {
    "hostObject.reference": {
      "type": "object",
      "properties": {
        "@type":         { "type": "string", "const": "host", "readOnly": true },
        "hostName":      { "type": "string", "format": "hostname", "readOnly": true }
      },
      "required": ["@type", "hostName"]
    }
  }
}
```

## Organisation Data Object

The following constraints cannot be expressed in JSON Schema and MUST be enforced by implementations:

- `id` MUST be a server-unique identifier conforming to the Identifier syntax.
- `status` MUST always contain at least one value. `pendingCreate`, `ok`, `hold`, and `terminated` are mutually exclusive. `ok` MAY only be combined with `linked`.
- `parent`, if present, MUST reference a known Organisation Object. Circular parent references MUST be rejected.
- `contacts` keys MUST be contact type values registered in the IANA "EPP Organisation Contact Types" registry ([@!RFC8543]).

### Create

Create request schema (create-only and read-write properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/organisationObject.create",
  "$defs": {
    "organisationObject.create": {
      "type": "object",
      "properties": {
        "@type":       { "type": "string", "const": "organisation" },
        "id":          { "$ref": "#/$defs/identifier" },
        "roles":       {
          "type": "object",
          "additionalProperties": { "$ref": "#/$defs/organisationRole" },
          "minProperties": 1
        },
        "parent":    { "$ref": "#/$defs/organisationObject.reference" },
        "contactInfo": { "$ref": "#/$defs/Card" },
        "contacts": {
          "type": "array",
          "items": { 
            "type": "object",
            "properties": {
              "label": { "type": "string" },
              "object": { "$ref": "#/$defs/contactObject.reference" }
            },
            "required": ["label", "object"]
           }
        }
      },
      "required": ["@type", "id", "roles"]      
    }
  }
}
```

### Read

Read response schema (read-write and read-only properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/organisationObject.read",
  "$defs": {
    "organisationObject.read": {
      "allOf": [
        { "$ref": "#/$defs/organisationObject.create" },
        {
          "properties": {
            "provMetadata": { "$ref": "#/$defs/provMetadata", "readOnly": true },
            "status": {
              "type": "array",
              "items": { "$ref": "#/$defs/status" },
              "readOnly": true
            },
            "users": {
              "type": "array",
              "items": { 
                "type": "object",
                "properties": {
                  "label": { "type": "string" },
                  "object": { "$ref": "#/$defs/userObject.reference" }
                },
                "required": ["label", "object"]
              }
            }
          },
          "required": ["provMetadata", "status"]
        }
      ]
    }
  }
}
```

### Update

Update request schema (read-write properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/organisationObject.update",
  "$defs": {
    "organisationObject.update": {
      "type": "object",
      "properties": {
        "@type":       { "type": "string", "const": "organisation" },
        "roles":       {
          "type": "object",
          "additionalProperties": { "$ref": "#/$defs/organisationRole" }
        },
        "parent":    { "$ref": "#/$defs/organisationObject.reference" },
        "contactInfo": { "$ref": "#/$defs/Card" },
        "contacts": {
            "type": "array",
            "items": { 
              "type": "object",
              "properties": {
                "label": { "type": "string" },
                "object": { "$ref": "#/$defs/contactObject.reference" }
              },
              "required": ["label", "object"]
            }
        },
        "status": {
              "type": "array",
              "items": { "$ref": "#/$defs/status" },
              "readOnly": true
        },
        "users":       {
          "type": "array",
          "items": { 
            "type": "object",
            "properties": {
              "label": { "type": "string" },
              "object": { "$ref": "#/$defs/userObject.reference" }
            },
            "required": ["label", "object"]
          }
        }
      },
      "required": ["@type"]
    }
  }
}
```

### Reference

Reference schema (identifier only):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/organisationObject.reference",
  "$defs": {
    "organisationObject.reference": {
      "type": "object",
      "properties": {
        "@type": { "type": "string", "const": "organisation", "readOnly": true },
        "id":    { "$ref": "#/$defs/identifier", "readOnly": true }
      },
      "required": ["@type", "id"]
    }
  }
}
```

## User Data Object

The User Data Object represents a user linked to an Organisation Object. The lifecycle of a User Object is bound to its owning Organisation Object.

Note: User status values are plain strings, not Status Objects.

### Create

Create request schema (create-only and read-write properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/userObject.create",
  "$defs": {
    "userObject.create": {
      "type": "object",
      "properties": {
        "@type":  { "type": "string", "const": "user" },
        "organisationId": { "$ref": "#/$defs/organisationObject.reference" },
        "details": { "$ref": "#/$defs/contactObject.reference" },
        "status": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["active", "suspended", "deactivated", "pending"]
          }
        },
        "description":  { "type": "string", "const": "user" }
      },
      "required": ["@type", "organisationId", "details"]
    }
  }
}
```

### Read

Read response schema (read-write and read-only properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/userObject.read",
  "$defs": {
    "userObject.read": {
      "type": "object",
      "properties": {
        "@type":  { "type": "string", "const": "user", "readOnly": true },
        "organisationId": { "$ref": "#/$defs/organisationObject.reference" },
        "userId": { "$ref": "#/$defs/identifier", "readOnly": true },
        "details": { "$ref": "#/$defs/contactObject.reference" },
        "status": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["active", "suspended", "deactivated", "pending"]
          }
        },
        "description":  { "type": "string", "const": "user" }
      },
      "required": ["@type", "userId", "details", "status"]
    }
  }
}
```

### Update

Update request schema (read-write properties):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/userObject.update",
  "$defs": {
    "userObject.update": {
      "type": "object",
      "properties": {
        "@type":  { "type": "string", "const": "user" },
        "details": { "$ref": "#/$defs/contactObject.reference" },
        "status": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["active", "suspended", "deactivated", "pending"]
          }
        }
      },
      "required": ["@type"]
    }
  }
}
```

### Reference

Reference schema (identifier only):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "#/$defs/userObject.reference",
  "$defs": {
    "userObject.reference": {
      "type": "object",
      "properties": {
        "@type":  { "type": "string", "const": "user", "readOnly": true },
        "id": { "$ref": "#/$defs/identifier", "readOnly": true }
      },
      "required": ["@type", "id"]
    }
  }
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
    "name": "example.example",
    "nameservers": [
        { "@type": "host", "hostName": "ns1.example.example" },
        { "@type": "host", "hostName": "ns2.example.example" }
    ],
    "registrant": { "@type": "contact", "id": "jd1234" },
    "contacts": [
        { "label": "admin", "object": { "@type": "contact", "id": "sh8013" } },
        { "label": "tech", "object": { "@type": "contact", "id": "sh8013" } }
    ],
    "authInfo": {
        "@type": "authInfo",
        "method": "authinfo",
        "authdata": "2fooBAR"
    },
    "processes": {
        "@type": "processes",
        "createProcess": [
            {
                "@type": "createProcess",
                "period": {
                    "@type": "period",
                    "value": 2,
                    "unit": "y"
                }
            }
        ]
    }
}
```

Example domain create response from a server with RGP support:

```json
{
    "@type": "domainName",
    "name": "example.example",
    "provMetadata": {
        "@type": "provMetadata",
        "repositoryId": "EXAMPLE1-REP",
        "spClientId": "ClientX",
        "crClientId": "ClientX",
        "crDate": "1999-04-03T22:00:00.0Z"
    },
    "status": [
        { "@type": "status", "label": "ok" },
        { "@type": "status", "label": "addPeriod" }
    ],
    "expiryDate": "2001-04-03T22:00:00.0Z"
}
```

### Create Process Data

Example Create Process Object for a two-year registration period, as embedded above in `processes.createProcess`:

```json
{
    "@type": "createProcess",
    "period": {
        "@type": "period",
        "value": 2,
        "unit": "y"
    }
}
```


### Read

Example domain read response:

```json
{
    "@type": "domainName",
    "name": "example.example",
    "provMetadata": {
        "@type": "provMetadata",
        "repositoryId": "EXAMPLE1-REP",
        "spClientId": "ClientX",
        "crClientId": "ClientY",
        "crDate": "1999-04-03T22:00:00.0Z",
        "upClientId": "ClientX",
        "upDate": "1999-12-03T09:00:00.0Z",
        "trDate": "2000-04-08T09:00:00.0Z"
    },
    "status": [
        { "@type": "status", "label": "ok" }
    ],
    "registrant": { "@type": "contact", "id": "jd1234" },
    "contacts": [
        { "label": "admin", "object": { "@type": "contact", "id": "sh8013" } },
        { "label": "tech", "object": { "@type": "contact", "id": "sh8013" } }
    ],
    "nameservers": [
        {
            "@type": "host",
            "hostName": "ns1.example.example"
        },
        {
            "@type": "host",
            "hostName": "ns2.example.example"
        }
    ],
    "subordinateHosts": [
        {
            "@type": "host",
            "hostName": "ns1.example.example"
        },
        {
            "@type": "host",
            "hostName": "ns2.example.example"
        }
    ],
    "expiryDate": "2005-04-03T22:00:00.0Z",
    "authInfo": {
        "@type": "authInfo",
        "method": "authinfo",
        "authdata": "2fooBAR"
    },
    "processes": {
        "@type": "processes",
        "createProcess": [
            {
                "@type": "createProcess",
                "period": {
                    "@type": "period",
                    "value": 2,
                    "unit": "y"
                }
            }
        ]
    }
}
```

### Update

Example domain update request (read-write properties):

```json
{
    "@type": "domainName",
    "registrant": { "@type": "contact", "id": "sh8013" },
    "authInfo": {
        "@type": "authInfo",
        "method": "authinfo",
        "authdata": "2BARfoo"
    }
}
```

Example domain update response:

```json
{
    "@type": "domainName",
    "name": "example.example",
    "provMetadata": {
        "@type": "provMetadata",
        "repositoryId": "EXAMPLE1-REP",
        "spClientId": "ClientX",
        "crClientId": "ClientY",
        "crDate": "1999-04-03T22:00:00.0Z",
        "upClientId": "ClientX",
        "upDate": "2000-01-15T09:00:00.0Z"
    },
    "status": [
        { "@type": "status", "label": "ok" }
    ],
    "registrant": { "@type": "contact", "id": "sh8013" }
}
```

### Delete

The domain delete operation takes the domain name as the resource identifier in the request. No request body is required.

Example domain delete response (minimal, server may return full representation):

```json
{
    "@type": "domainName",
    "name": "example.example",
    "provMetadata": {
        "@type": "provMetadata",
        "repositoryId": "EXAMPLE1-REP",
        "spClientId": "ClientX"
    }
}
```

### Renew

The renew operation creates a Renew Process Object. The optional `expiryDate` in the request is the *current* expiry date, sent by the client for server-side validation to prevent duplicate renewals. The response returns a Renew Process Object containing the *new* expiry date.

Example domain renew request:

```json
{
    "@type": "renewProcess",
    "expiryDate": "2005-04-03T22:00:00.0Z",
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
    "@type": "renewProcess",
    "expiryDate": "2010-04-03T22:00:00.0Z"
}
```

### Transfer Request

Authorization information for the transfer MUST be conveyed using the `RPP-Authorization` HTTP header (see Rule 21), not in the JSON request body.

Example domain transfer request (pull transfer)

```json
{
    "@type": "transferProcess",
    "transferDir": "pull",
    "transferPeriod": {
        "@type": "period",
        "value": 1,
        "unit": "y"
    }
}
```

Example domain transfer response (Transfer Process Object):

```json
{
    "@type": "transferProcess",
    "trStatus": "pending",
    "transferDir": "pull",
    "reqClientId": "ClientX",
    "requestDate": "2000-06-08T22:00:00.0Z",
    "actClientId": "ClientY",
    "actionDate": "2000-06-13T22:00:00.0Z",
    "expiryDate": "2002-09-08T22:00:00.0Z"
}
```

### Transfer Query

Example domain transfer query response (Transfer Process Object):

```json
{
    "@type": "transferProcess",
    "trStatus": "pending",
    "transferDir": "pull",
    "reqClientId": "ClientX",
    "requestDate": "2000-06-06T22:00:00.0Z",
    "actClientId": "ClientY",
    "actionDate": "2000-06-11T22:00:00.0Z",
    "expiryDate": "2002-09-08T22:00:00.0Z"
}
```

### Transfer Approve

The Transfer approve operation has request body with an empty JSON object, the server can identify the transfer process to be approved based on the request URL and the authenticated client's permissions.

Example domain transfer approve request with empty JSON object:

```json
{ 
  "@type": "transferProcess"
}
```
<!-- Is this an empty response? or should we use "{}"? then validation script complains-->

The response is the Transfer Process Object, similar to the transfer create and query responses.

### Transfer Cancel

The Transfer cancel operation has an empty request body, the server can identify the transfer process to be cancelled based on the request URL and the authenticated client's permissions.

The response is the Transfer Process Object, similar to the transfer create and query responses.

### Transfer Reject

Example domain transfer reject request

```json
{
    "@type": "transferProcess",
    "reason": "Client rejected the transfer request."
}
```

The transfer reject response is the Transfer Process Object, similar to the transfer create and query responses.

### Restore Request

Example domain restore request (without inline report; object transitions to `pendingRestore` state):

```json
{
    "@type": "restoreProcess"
}
```

Example domain restore response (Restore Process Object, server requires a report):

```json
{
    "@type": "restoreProcess",
    "restoreStatus": "pendingRestore",
    "requestDate": "2025-01-20T15:30:00.0Z",
    "reportDueDate": "2025-01-27T15:30:00.0Z"
}
```

Example domain restore request with inline restore report (single-step; object restored immediately):

```json
{
    "@type": "restoreProcess",
    "restoreReport": {
        "@type": "restoreReport",
        "preData": "Domain example.example was registered on 2024-01-15 with registrant jd1234.",
        "postData": "Domain example.example is being restored with the same registration data.",
        "deleteTime": "2025-01-10T12:00:00.0Z",
        "restoreTime": "2025-01-20T15:30:00.0Z",
        "restoreReason": "Domain deleted in error by client operator.",
        "statements": [
            "The information in this report is true to the best of my knowledge.",
            "I have a valid reason for restoring this domain name."
        ]
    }
}
```

Example domain restore response with inline report (Restore Process Object, immediately restored):

```json
{
    "@type": "restoreProcess",
    "restoreStatus": "restored",
    "requestDate": "2025-01-20T15:30:00.0Z",
    "reportDate": "2025-01-20T15:30:00.0Z"
}
```

### Restore Report

Example domain restore report request:

```json
{
    "@type": "restoreProcess",
    "restoreReport": {
        "@type": "restoreReport",
        "preData": "Domain example.example was registered on 2024-01-15 with registrant jd1234.",
        "postData": "Domain example.example is being restored with the same registration data.",
        "deleteTime": "2025-01-10T12:00:00.0Z",
        "restoreTime": "2025-01-20T15:30:00.0Z",
        "restoreReason": "Domain deleted in error by client operator.",
        "statements": [
            "The information in this report is true to the best of my knowledge.",
            "I have a valid reason for restoring this domain name."
        ]
    }
}
```

Example domain restore report response (Restore Process Object):

```json
{
    "@type": "restoreProcess",
    "restoreStatus": "restored",
    "requestDate": "2025-01-20T15:30:00.0Z",
    "reportDate": "2025-01-22T09:15:00.0Z"
}
```

### Restore Query

The Restore Query operation takes no request body (Parameters: None).

Example domain restore query response (Restore Process Object, object in `pendingRestore` state):

```json
{
    "@type": "restoreProcess",
    "restoreStatus": "pendingRestore",
    "requestDate": "2025-01-20T15:30:00.0Z",
    "reportDueDate": "2025-01-27T15:30:00.0Z"
}
```

Example domain restore query response (Restore Process Object, object restored):

```json
{
    "@type": "restoreProcess",
    "restoreStatus": "restored",
    "requestDate": "2025-01-20T15:30:00.0Z",
    "reportDate": "2025-01-22T09:15:00.0Z"
}
```

## Contact

### Create

Example contact create request:

```json
{
    "@type": "contact",
    "id": "jd1234",
    "contactInfo": {
        "@type": "Card",
        "version": "2.0",
        "kind": "individual",
        "name": {
            "full": "John Doe",
            "components": [
                { "kind": "given",   "value": "John" },
                { "kind": "surname", "value": "Doe" }
            ]
        },
        "organizations": {
            "org": { "name": "Example Inc." }
        },
        "addresses": {
            "addr": {
                "components": [
                    { "kind": "name",     "value": "123 Example Dr., Suite 100" },
                    { "kind": "locality", "value": "Dulles" },
                    { "kind": "region",   "value": "VA" },
                    { "kind": "postcode", "value": "20166-6503" },
                    { "kind": "country",  "value": "United States" }
                ],
                "countryCode": "US"
            }
        },
        "phones": {
            "voice": { "number": "tel:+1-703-555-5555" },
            "fax":   { "features": { "fax": true }, "number": "tel:+1-703-555-5556" }
        },
        "emails": {
            "email": { "address": "jdoe@example.example" }
        }
    },
    "authInfo": {
        "@type": "authInfo",
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
    "provMetadata": {
        "@type": "provMetadata",
        "repositoryId": "JD1234-REP",
        "spClientId": "ClientX",
        "crClientId": "ClientX",
        "crDate": "1999-04-03T22:00:00.0Z"
    },
    "status": [
        { "@type": "status", "label": "ok" }
    ],
    "contactInfo": {
        "@type": "Card",
        "version": "2.0",
        "kind": "individual",
        "name": {
            "full": "John Doe",
            "components": [
                { "kind": "given",   "value": "John" },
                { "kind": "surname", "value": "Doe" }
            ]
        },
        "organizations": {
            "org": { "name": "Example Inc." }
        },
        "addresses": {
            "addr": {
                "components": [
                    { "kind": "name",     "value": "123 Example Dr., Suite 100" },
                    { "kind": "locality", "value": "Dulles" },
                    { "kind": "region",   "value": "VA" },
                    { "kind": "postcode", "value": "20166-6503" },
                    { "kind": "country",  "value": "United States" }
                ],
                "countryCode": "US"
            }
        },
        "phones": {
            "voice": { "number": "tel:+1-703-555-5555" },
            "fax":   { "features": { "fax": true }, "number": "tel:+1-703-555-5556" }
        },
        "emails": {
            "email": { "address": "jdoe@example.example" }
        }
    }
}
```

### Read

Example contact read response:

```json
{
    "@type": "contact",
    "id": "jd1234",
    "provMetadata": {
        "@type": "provMetadata",
        "repositoryId": "JD1234-REP",
        "spClientId": "ClientX",
        "crClientId": "ClientX",
        "crDate": "1999-04-03T22:00:00.0Z",
        "upClientId": "ClientX",
        "upDate": "2000-01-15T09:00:00.0Z"
    },
    "status": [
        { "@type": "status", "label": "ok" }
    ],
    "contactInfo": {
        "@type": "Card",
        "version": "2.0",
        "kind": "individual",
        "name": {
            "full": "John Doe",
            "components": [
                { "kind": "given",   "value": "John" },
                { "kind": "surname", "value": "Doe" }
            ]
        },
        "organizations": {
            "org": { "name": "Example Inc." }
        },
        "addresses": {
            "addr": {
                "components": [
                    { "kind": "name",     "value": "123 Example Dr., Suite 100" },
                    { "kind": "locality", "value": "Dulles" },
                    { "kind": "region",   "value": "VA" },
                    { "kind": "postcode", "value": "20166-6503" },
                    { "kind": "country",  "value": "United States" }
                ],
                "countryCode": "US"
            }
        },
        "phones": {
            "voice": { "number": "tel:+1-703-555-5555" }
        },
        "emails": {
            "email": { "address": "jdoe@example.example" }
        }
    }
}
```

### Update

Example contact update request:

```json
{
    "@type": "contact",
    "contactInfo": {
        "@type": "Card",
        "version": "2.0",
        "addresses": {
            "addr": {
                "components": [
                    { "kind": "name",     "value": "456 New Street, Suite 200" },
                    { "kind": "locality", "value": "Reston" },
                    { "kind": "region",   "value": "VA" },
                    { "kind": "postcode", "value": "20190" },
                    { "kind": "country",  "value": "United States" }
                ],
                "countryCode": "US"
            }
        },
        "phones": {
            "voice": { "number": "tel:+1-703-555-5556" }
        },
        "emails": {
            "email": { "address": "jdoe-new@example.example" }
        }
    }
}
```

Example contact update response:

```json
{
    "@type": "contact",
    "id": "jd1234",
    "provMetadata": {
        "@type": "provMetadata",
        "repositoryId": "JD1234-REP",
        "spClientId": "ClientX",
        "crClientId": "ClientX",
        "crDate": "1999-04-03T22:00:00.0Z",
        "upClientId": "ClientX",
        "upDate": "2025-06-01T10:00:00.0Z"
    },
    "status": [
        { "@type": "status", "label": "ok" }
    ],
    "contactInfo": {
        "@type": "Card",
        "version": "2.0",
        "kind": "individual",
        "name": {
            "full": "John Doe",
            "components": [
                { "kind": "given",   "value": "John" },
                { "kind": "surname", "value": "Doe" }
            ]
        },
        "organizations": {
            "org": { "name": "Example Inc." }
        },
        "addresses": {
            "addr": {
                "components": [
                    { "kind": "name",     "value": "456 New Street, Suite 200" },
                    { "kind": "locality", "value": "Reston" },
                    { "kind": "region",   "value": "VA" },
                    { "kind": "postcode", "value": "20190" },
                    { "kind": "country",  "value": "United States" }
                ],
                "countryCode": "US"
            }
        },
        "phones": {
            "voice": { "number": "tel:+1-703-555-5556" }
        },
        "emails": {
            "email": { "address": "jdoe-new@example.example" }
        }
    }
}
```

### Delete

The contact delete operation takes the contact identifier as the resource identifier. No request body is required.

### Transfer Request

Authorization information for the transfer MUST be conveyed using the `RPP-Authorization` HTTP header (see Rule 21), not in the JSON request body.

Example contact transfer request (pull transfer)

```json
{
    "@type": "transferProcess", 
    "transferDir": "pull"
}
```

Example contact transfer response (Transfer Process Object):

```json
{
    "@type": "transferProcess",
    "trStatus": "pending",
    "transferDir": "pull",
    "reqClientId": "ClientX",
    "requestDate": "2000-06-08T22:00:00.0Z",
    "actClientId": "ClientY",
    "actionDate": "2000-06-13T22:00:00.0Z"
}
```

### Transfer Query

Example contact transfer query response (Transfer Process Object):

```json
{
    "@type": "transferProcess",
    "trStatus": "pending",
    "transferDir": "pull",
    "reqClientId": "ClientX",
    "requestDate": "2000-06-06T22:00:00.0Z",
    "actClientId": "ClientY",
    "actionDate": "2000-06-11T22:00:00.0Z"
}
```

### Transfer Cancel / Approve

Transfer cancel and approve responses return the Transfer Process Object. The response structure is the same as the Transfer Query response above. The `trStatus` value reflects the outcome of the operation (e.g. `"clientCancelled"`, `"clientRejected"`, or `"clientApproved"`).

### Transfer Reject

Example Contact Transfer Reject request

```json
{
    "@type": "transferProcess",
    "reason": "Client rejected the transfer request."
}
```

The transfer reject response is the Transfer Process Object, similar to the transfer create and query responses.

## Host

### Create

Example host create request:

```json
{
    "@type": "host",
    "hostName": "ns1.example.example",
    "dns": {
        "@type": "dnsData",
        "records": [
            {
                "@type": "dnsRecord",
                "name": "@",
                "type": "ns",
                "rdata": { "nsdname": "ns1.example.example." }
            },
            {
                "@type": "dnsRecord",
                "name": "ns1.example.example.",
                "type": "a",
                "rdata": { "address": "192.0.2.1" }
            },
            {
                "@type": "dnsRecord",
                "name": "ns1.example.example.",
                "type": "aaaa",
                "rdata": { "address": "2001:db8::1" }
            }
        ]
    }
}
```

Example host create response:

```json
{
    "@type": "host",
    "hostName": "ns1.example.example",
    "provMetadata": {
        "@type": "provMetadata",
        "repositoryId": "NS1EXAMPLE-REP",
        "spClientId": "ClientX",
        "crClientId": "ClientX",
        "crDate": "1999-04-03T22:00:00.0Z"
    },
    "status": [
        { "@type": "status", "label": "ok" }
    ],
    "dns": {
        "@type": "dnsData",
        "records": [
            {
                "@type": "dnsRecord",
                "name": "@",
                "type": "ns",
                "rdata": { "nsdname": "ns1.example.example." }
            },
            {
                "@type": "dnsRecord",
                "name": "ns1.example.example.",
                "type": "a",
                "rdata": { "address": "192.0.2.1" }
            },
            {
                "@type": "dnsRecord",
                "name": "ns1.example.example.",
                "type": "aaaa",
                "rdata": { "address": "2001:db8::1" }
            }
        ]
    }
}
```

### Read

Example host read response:

```json
{
    "@type": "host",
    "hostName": "ns1.example.example",
    "provMetadata": {
        "@type": "provMetadata",
        "repositoryId": "NS1EXAMPLE-REP",
        "spClientId": "ClientX",
        "crClientId": "ClientY",
        "crDate": "1999-04-03T22:00:00.0Z"
    },
    "status": [
        { "@type": "status", "label": "ok" }
    ],
    "dns": {
        "@type": "dnsData",
        "records": [
            {
                "@type": "dnsRecord",
                "name": "@",
                "type": "ns",
                "rdata": { "nsdname": "ns1.example.example." }
            },
            {
                "@type": "dnsRecord",
                "name": "ns1.example.example.",
                "type": "a",
                "rdata": { "address": "192.0.2.1" }
            }
        ]
    }
}
```

### Update

Example host update request:

```json
{
    "@type": "host",
    "hostName": "ns1.example.example",
    "dns": {
        "@type": "dnsData",
        "records": [
            {
                "@type": "dnsRecord",
                "name": "@",
                "type": "ns",
                "rdata": { "nsdname": "ns1.example.example." }
            },
            {
                "@type": "dnsRecord",
                "name": "ns1.example.example.",
                "type": "a",
                "rdata": { "address": "198.51.100.1" }
            }
        ]
    }
}
```

### Delete

The host delete operation takes the host name as the resource identifier. No request body is required. The server SHOULD reject the request if the host object is associated with any domain name objects.

### Restore Request

Example host restore request (without inline report; object transitions to `pendingRestore` state):

```json
{
  "@type": "restoreProcess"
}
```

Example host restore request response (Restore Process Object, server requires a report):

```json
{
    "@type": "restoreProcess",
    "restoreStatus": "pendingRestore",
    "requestDate": "2025-01-20T15:30:00.0Z",
    "reportDueDate": "2025-01-27T15:30:00.0Z"
}
```

Example host restore request with inline restore report (single-step; object restored immediately):

```json
{
    "@type": "restoreProcess",
    "restoreReport": {
        "@type": "restoreReport",
        "preData": "Host ns1.example.example was registered on 2024-01-15 by ClientX.",
        "postData": "Host ns1.example.example is being restored with the same registration data.",
        "deleteTime": "2025-01-10T12:00:00.0Z",
        "restoreTime": "2025-01-20T15:30:00.0Z",
        "restoreReason": "Host deleted in error by client operator.",
        "statements": [
            "The information in this report is true to the best of my knowledge.",
            "I have a valid reason for restoring this host object."
        ]
    }
}
```

Example host restore response with inline report (Restore Process Object, immediately restored):

```json
{
    "@type": "restoreProcess",
    "restoreStatus": "restored",
    "requestDate": "2025-01-20T15:30:00.0Z",
    "reportDate": "2025-01-20T15:30:00.0Z"
}
```

### Restore Report

Example host restore report request:

```json
{
    "@type": "restoreProcess",
    "restoreReport": {
        "@type": "restoreReport",
        "preData": "Host ns1.example.example was registered on 2024-01-15 by ClientX.",
        "postData": "Host ns1.example.example is being restored with the same registration data.",
        "deleteTime": "2025-01-10T12:00:00.0Z",
        "restoreTime": "2025-01-20T15:30:00.0Z",
        "restoreReason": "Host deleted in error by client operator.",
        "statements": [
            "The information in this report is true to the best of my knowledge.",
            "I have a valid reason for restoring this host object."
        ]
    }
}
```

Example host restore report response (Restore Process Object):

```json
{
    "@type": "restoreProcess",
    "restoreStatus": "restored",
    "requestDate": "2025-01-20T15:30:00.0Z",
    "reportDate": "2025-01-22T09:15:00.0Z"
}
```

### Restore Query

The Restore Query operation takes no request body (Parameters: None).

Example host restore query response (Restore Process Object, object in `pendingRestore` state):

```json
{
    "@type": "restoreProcess",
    "restoreStatus": "pendingRestore",
    "requestDate": "2025-01-20T15:30:00.0Z",
    "reportDueDate": "2025-01-27T15:30:00.0Z"
}
```

Example host restore query response (Restore Process Object, object restored):

```json
{
    "@type": "restoreProcess",
    "restoreStatus": "restored",
    "requestDate": "2025-01-20T15:30:00.0Z",
    "reportDate": "2025-01-22T09:15:00.0Z"
}
```

## Organisation

### Create

Example organisation create request:

```json
{
    "@type": "organisation",
    "id": "ORG-12345",
    "roles": { "registrar": 
        {
            "@type": "organisationRole",
            "roleId": "1234"
        }
    },
    "parent": { "@type": "organisation", "id": "ORG-9999" },
    "contactInfo": {
        "@type": "Card",
        "version": "2.0",
        "kind": "org",
        "name": {
            "full": "Example Registrar Inc."
        },
        "addresses": {
            "addr": {
                "components": [
                    { "kind": "name",     "value": "Meander 501" },
                    { "kind": "locality", "value": "Arnhem" },
                    { "kind": "region",   "value": "Gelderland" },
                    { "kind": "postcode", "value": "6825MD" },
                    { "kind": "country",  "value": "Netherlands" }
                ],
                "countryCode": "NL"
            }
        },
        "emails": {
            "email": { "address": "registrar@example.example" }
        }
    },
    "contacts": [
        { "label": "admin", "object": { "@type": "contact", "id": "CID-1001" } },
        { "label": "tech", "object": { "@type": "contact", "id": "CID-1002" } }
    ]
}
```

Example organisation create response:

```json
{
    "@type": "organisation",
    "id": "ORG-12345",
    "provMetadata": {
        "@type": "provMetadata",
        "repositoryId": "ORG12345-REP",
        "spClientId": "ClientX",
        "crClientId": "ClientX",
        "crDate": "2025-03-15T10:00:00.0Z"
    },
    "status": [
        { "@type": "status", "label": "ok" }
    ],
    "roles": { "registrar":
        {
            "@type": "organisationRole",
            "status": ["ok"],
            "roleId": "1234"
        }
    },
    "parent": { "@type": "organisation", "id": "ORG-9999" },
    "contactInfo": {
        "@type": "Card",
        "version": "2.0",
        "kind": "org",
        "name": {
            "full": "Example Registrar Inc."
        },
        "addresses": {
            "addr": {
               "components": [
                    { "kind": "name",     "value": "Meander 501" },
                    { "kind": "locality", "value": "Arnhem" },
                    { "kind": "region",   "value": "Gelderland" },
                    { "kind": "postcode", "value": "6825MD" },
                    { "kind": "country",  "value": "Netherlands" }
                ],
                "countryCode": "NL"
            }
        },
        "emails": {
            "email": { "address": "registrar@example.example" }
        }
    },
    "contacts": [
        { "label": "admin", "object": { "@type": "contact", "id": "CID-1001" } },
        { "label": "tech", "object": { "@type": "contact", "id": "CID-1002" } }
    ],
    "users": [
        { "label": "admin", "object": { "@type": "user", "id": "UID-5001" } }
    ]
}
```

### Read

Example organisation read response:

```json
{
    "@type": "organisation",
    "id": "ORG-12345",
    "provMetadata": {
        "@type": "provMetadata",
        "repositoryId": "ORG12345-REP",
        "spClientId": "ClientX",
        "crClientId": "ClientX",
        "crDate": "2025-03-15T10:00:00.0Z",
        "upClientId": "ClientX",
        "upDate": "2025-06-01T08:30:00.0Z"
    },
    "status": [
        { "@type": "status", "label": "linked" }
    ],
    "roles": { "registrar":
        {
            "@type": "organisationRole",
            "status": ["ok"],
            "roleId": "1234"
        }
    },
    "parent": { "@type": "organisation", "id": "ORG-9999" },
    "contactInfo": {
        "@type": "Card",
        "version": "2.0",
        "kind": "org",
        "name": {
            "full": "Example Registrar Inc."
        },
        "addresses": {
            "addr": {
                "components": [
                    { "kind": "name",     "value": "Meander 501" },
                    { "kind": "locality", "value": "Arnhem" },
                    { "kind": "region",   "value": "Gelderland" },
                    { "kind": "postcode", "value": "6825MD" },
                    { "kind": "country",  "value": "Netherlands" }
                ],
                "countryCode": "NL"
            }
        },
        "emails": {
            "email": { "address": "registrar@example.example" }
        }
    },
    "contacts": [
        { "label": "admin", "object": { "@type": "contact", "id": "CID-1001" } },
        { "label": "tech", "object": { "@type": "contact", "id": "CID-1002" } }
    ],
    "users": [
        { "label": "admin", "object": { "@type": "user", "id": "UID-5001" } }
    ]
}
```

### Update

Example organisation update request:

```json
{
    "@type": "organisation",
    "roles": { "registrar":
        {
            "@type": "organisationRole",
            "status": ["clientLinkProhibited"],
            "roleId": "1234"
        }
    },
    "status": [
        { "@type": "status", "label": "clientLinkProhibited" }
    ],
    "contacts": [
        { "label": "admin", "object": { "@type": "contact", "id": "CID-2001" } },
        { "label": "tech", "object": { "@type": "contact", "id": "CID-2002" } }
    ]
}
```

### Delete

The organisation delete operation takes the organisation identifier as the resource identifier. No request body is required. The server MUST reject the request if the organisation object is associated with any other objects.

### Reference

Example organisation reference (used when referencing an organisation from another object):

```json
{
    "@type": "organisation",
    "id": "ORG-12345"
}
```

## User

### Create

Example user create request:

```json
{
    "@type": "user",
    "details": { "@type": "contact", "id": "USER-1234" },
    "status": ["active"]
}
```

Example user create response:

```json
{
    "@type": "user",
    "userId": "UID-5001",
    "details": { "@type": "contact", "id": "USER-1234" },
    "status": ["active"]
}
```

### Read

Example user read response:

```json
{
    "@type": "user",
    "organisationId": { "@type": "organisation", "id": "ORG-12345" },
    "userId": "UID-5001",
    "details": { "@type": "contact", "id": "USER-1234" },
    "status": ["active"]
}
```

### Update

Example user update request (suspend the user):

```json
{
    "@type": "user",
    "status": ["suspended"]
}
```

### Delete

The user delete operation takes the user identifier as the resource identifier in the context of the owning organisation. No request body is required.

### Reference

Example user reference (used when referencing a user from an organisation object):

```json
{
    "@type": "user",
    "id": "UID-5001"
}
```

# IANA Considerations

TODO

# Internationalization Considerations

TODO

# Security Considerations

TODO

# Acknowledgments

TODO

# Change History

## Version 02 to 03

- Added schema and examples for Transfer approve/reject/cancel operations (Issue #28)
- Added Organisation and User Object JSON schemas and examples. (Issue #57)
- Added schema and examples for the Renew Process Object. (Issue #45)
- Add representation for embedding of process data in uniform interface operations (especially create). (Issue #60)
- define rules for External Type Embedding.
- Add JSContact as External Type Embedding (Issue #43).

## Version 01 to 02

- Adjust rule 19 and all schemas to match it.

## Version 00 to 01

- Updated all examples and schemas to be based on RPP Data Object and no longer on EPP XML schemas. (Issue #15)
- Updated labelled and dictionary aggregation rules (Issue #17)
- Added required "@type" property to all JSON Schema definitions. (Issue #20)
- Updated all example domain names to use the .example TLD. (Issue #26)

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

<reference anchor="ISO3166-1" target="https://www.iso.org/standard/72482.html">
  <front>
    <title>Codes for the representation of names of countries and their subdivisions - Part 1: Country code</title>
    <author>
      <organization>International Organization for Standardization</organization>
    </author>
    <date year="2020"/>
  </front>
  <seriesInfo name="ISO" value="3166-1:2020"/>
</reference>

<reference anchor="RFC3915" target="https://www.rfc-editor.org/rfc/rfc3915">
  <front>
    <title>Domain Registry Grace Period Mapping for the Extensible Provisioning Protocol (EPP)</title>
    <author initials="S." surname="Hollenbeck" fullname="Scott Hollenbeck"/>
    <date year="2004" month="09"/>
  </front>
  <seriesInfo name="RFC" value="3915"/>
  <seriesInfo name="DOI" value="10.17487/RFC3915"/>
</reference>
