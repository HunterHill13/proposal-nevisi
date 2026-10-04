#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
schema_validator.py - Pure Python JSON Schema Validator (Draft-07 Compatible)
Proposal-Nevisi Engine v8.2 (Universal Biomedical Architecture)

Validates dictionary data structures against JSON schema files without external third-party dependencies.
Enforces types, required properties, enums, nested properties, array items, and pattern constraints.
"""

import re
import json
import os
from typing import Dict, List, Any, Tuple, Optional

class SchemaValidationError(Exception):
    """Raised when data fails schema constraints."""
    pass

class SchemaValidator:
    """Draft-07 compatible JSON Schema validator operating via Python standard library."""

    @classmethod
    def load_schema(cls, schema_path_or_name: str) -> Dict[str, Any]:
        """Loads JSON schema from path or relative schemas directory."""
        if os.path.exists(schema_path_or_name):
            with open(schema_path_or_name, "r", encoding="utf-8") as f:
                return json.load(f)
        
        # Look in schemas/
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "schemas"))
        cand = os.path.join(base_dir, schema_path_or_name)
        if os.path.exists(cand):
            with open(cand, "r", encoding="utf-8") as f:
                return json.load(f)
                
        if not schema_path_or_name.endswith(".json"):
            cand2 = os.path.join(base_dir, f"{schema_path_or_name}.json")
            if os.path.exists(cand2):
                with open(cand2, "r", encoding="utf-8") as f:
                    return json.load(f)

        raise FileNotFoundError(f"Schema not found: {schema_path_or_name}")

    @classmethod
    def validate(cls, instance: Any, schema: Dict[str, Any], path: str = "root") -> List[str]:
        """Recursively validates an instance against schema; returns list of error messages."""
        errors: List[str] = []

        # 1. Type validation
        expected_type = schema.get("type")
        if expected_type:
            types = [expected_type] if isinstance(expected_type, str) else expected_type
            match_found = False
            for t in types:
                if t == "object" and isinstance(instance, dict):
                    match_found = True
                    break
                elif t == "array" and isinstance(instance, list):
                    match_found = True
                    break
                elif t == "string" and isinstance(instance, str):
                    match_found = True
                    break
                elif t == "integer" and isinstance(instance, int) and not isinstance(instance, bool):
                    match_found = True
                    break
                elif t == "number" and isinstance(instance, (int, float)) and not isinstance(instance, bool):
                    match_found = True
                    break
                elif t == "boolean" and isinstance(instance, bool):
                    match_found = True
                    break
                elif t == "null" and instance is None:
                    match_found = True
                    break
            
            if not match_found:
                errors.append(f"[{path}] Expected type '{expected_type}', got '{type(instance).__name__}' (value: {repr(instance)[:50]})")
                return errors

        # 2. Enum validation
        if "enum" in schema:
            if instance not in schema["enum"]:
                errors.append(f"[{path}] Value {repr(instance)} is not one of allowed enum values: {schema['enum']}")

        # 3. String constraints
        if isinstance(instance, str):
            if "minLength" in schema and len(instance) < schema["minLength"]:
                errors.append(f"[{path}] String length {len(instance)} is less than minLength {schema['minLength']}")
            if "maxLength" in schema and len(instance) > schema["maxLength"]:
                errors.append(f"[{path}] String length {len(instance)} is greater than maxLength {schema['maxLength']}")
            if "pattern" in schema and not re.search(schema["pattern"], instance):
                errors.append(f"[{path}] String does not match required regex pattern: {schema['pattern']}")

        # 4. Numeric constraints
        if isinstance(instance, (int, float)) and not isinstance(instance, bool):
            if "minimum" in schema and instance < schema["minimum"]:
                errors.append(f"[{path}] Numeric value {instance} is less than minimum {schema['minimum']}")
            if "maximum" in schema and instance > schema["maximum"]:
                errors.append(f"[{path}] Numeric value {instance} is greater than maximum {schema['maximum']}")

        # 5. Object validation
        if isinstance(instance, dict):
            # Check required fields
            for req in schema.get("required", []):
                if req not in instance:
                    errors.append(f"[{path}] Missing required property: '{req}'")

            # Check properties
            props = schema.get("properties", {})
            for key, val in instance.items():
                if key in props:
                    errors.extend(cls.validate(val, props[key], path=f"{path}.{key}"))
                elif schema.get("additionalProperties") is False:
                    errors.append(f"[{path}] Additional property '{key}' is not allowed by schema.")

        # 6. Array validation
        if isinstance(instance, list):
            if "minItems" in schema and len(instance) < schema["minItems"]:
                errors.append(f"[{path}] Array items count {len(instance)} is less than minItems {schema['minItems']}")
            if "items" in schema and isinstance(schema["items"], dict):
                for idx, item in enumerate(instance):
                    errors.extend(cls.validate(item, schema["items"], path=f"{path}[{idx}]"))

        return errors

    @classmethod
    def is_valid(cls, instance: Any, schema_or_name: Any) -> bool:
        """Convenience method returning True if data is valid against schema."""
        if isinstance(schema_or_name, str):
            schema = cls.load_schema(schema_or_name)
        else:
            schema = schema_or_name
        errors = cls.validate(instance, schema)
        return len(errors) == 0

    @classmethod
    def assert_valid(cls, instance: Any, schema_or_name: Any):
        """Raises SchemaValidationError if instance is invalid."""
        if isinstance(schema_or_name, str):
            schema = cls.load_schema(schema_or_name)
        else:
            schema = schema_or_name
        errors = cls.validate(instance, schema)
        if errors:
            raise SchemaValidationError(f"Schema validation failed ({len(errors)} errors):\n" + "\n".join(errors[:10]))
