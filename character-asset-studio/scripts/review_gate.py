#!/usr/bin/env python3
"""Validate a requirement-by-requirement image review against a frozen brief."""
import argparse
import hashlib
import json
import math
from pathlib import Path


def evaluate(contract, review, image):
    criteria = contract.get('criteria', [])
    if not isinstance(criteria, list) or not criteria:
        raise ValueError('contract needs a nonempty criteria array')
    ids = [item['id'] for item in criteria]
    if any(not isinstance(key, str) or not key.strip() for key in ids) or len(set(ids)) != len(ids):
        raise ValueError('criterion IDs must be unique nonempty strings')
    threshold = contract.get('threshold', 95)
    if isinstance(threshold, bool) or not isinstance(threshold, (int, float)) or not 0 <= threshold <= 100:
        raise ValueError('threshold must be between 0 and 100')
    digest = hashlib.sha256(image.read_bytes()).hexdigest()
    contract_digest = hashlib.sha256(json.dumps(contract, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    issues = []
    if review.get('imageSha256') != digest:
        issues.append('review does not match the current image bytes')
    if review.get('contractSha256') != contract_digest:
        issues.append('review does not match the frozen contract')
    entries = review.get('checks', [])
    if not isinstance(entries, list):
        raise ValueError('checks must be an array')
    checks = {}
    for item in entries:
        key = item['id']
        if key in checks or key not in ids:
            issues.append(f'duplicate or unknown check: {key}')
        checks[key] = item
    earned = total = 0
    corrections = []
    for criterion in criteria:
        key = criterion['id']
        if not str(criterion.get('requirement', '')).strip():
            raise ValueError(f'{key} needs a requirement')
        weight = criterion.get('weight', 1)
        if isinstance(weight, bool) or not isinstance(weight, (int, float)) or not math.isfinite(weight) or weight <= 0:
            raise ValueError(f'{key} needs a positive finite weight')
        total += weight
        check = checks.get(key, {})
        passed = check.get('status') == 'pass' and bool(str(check.get('evidence') or '').strip())
        if check.get('status') not in ('pass', 'fail', 'unknown'):
            issues.append(f'{key}: missing or invalid review status')
        if passed:
            earned += weight
        else:
            corrections.append({'id': key, 'requirement': criterion['requirement'], 'observation': check.get('evidence', 'Unreviewed'), 'correction': check.get('correction', '')})
            if criterion.get('critical', True):
                issues.append(f'{key}: critical requirement has not passed with evidence')
    if review.get('structuralQa', {}).get('status') != 'pass':
        issues.append('structural QA has not passed')
    if not review.get('structuralQa', {}).get('evidence'):
        issues.append('structural QA needs evidence')
    score = 100 * earned / total
    if score < threshold:
        issues.append(f'score {score:.1f} is below {threshold}')
    return {'approved': not issues, 'score': round(score, 2), 'threshold': threshold, 'imageSha256': digest,
            'contractSha256': contract_digest, 'issues': issues, 'corrections': corrections,
            'scoreMeaning': 'Weighted coverage of evidence-backed passed criteria; visual judgments are supplied by the reviewing agent.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('contract', type=Path)
    parser.add_argument('review', type=Path)
    parser.add_argument('image', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        result = evaluate(json.loads(args.contract.read_text()), json.loads(args.review.read_text()), args.image)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        result = {'approved': False, 'issues': [str(exc)]}
    rendered = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end='')
    return 0 if result['approved'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
