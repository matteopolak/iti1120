from sys import stderr

import nonrec
import rec

CASES = (
	(
		'sumIntegers', nonrec.sumIntegers, rec.sum_integers,
		(1, 2, 3, 4, 100, 274, 476, 520)
	), (
		'sequence',
		nonrec.sequence,
		rec.sequence,
		(1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
	), (
		'check',
		nonrec.check,
		rec.check,
		(
			'',
			'aaaabaaaa',
			'87asdakjsf',
			'a',
			'aa',
			'ab',
			'aba',
			'abba',
			'abcba',
			'abcde',
			'abcdeedcba',
			'abcdeedcb',
			'abcdeedc',
		),
	)
)

for name, nonrec_func, rec_func, args in CASES:
	print(f'Running test for {name}()...')

	for arg in args:
		nonrec_result = nonrec_func(arg)
		rec_result = rec_func(arg)  # type: ignore

		if nonrec_result != rec_result:
			print(
				f'[{name}] expected {nonrec_result} but got {rec_result} for {arg}',
				file=stderr
			)
		else:
			print(f'[{name}] {arg} OK ({rec_result})')
