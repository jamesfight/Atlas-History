import json
import tempfile
import unittest
from pathlib import Path
from atlas import Archive


class Tests(unittest.TestCase):
    def setUp(self):
        self.a = Archive(':memory:')
        self.a.add('a', 'c', 'Old chat', 'user', 'Salmon research: me@example.com')

    def tearDown(self):
        self.a.db.close()

    def test_retrieval_and_deletion(self):
        self.assertEqual(self.a.context('salmon')['sources'][0]['id'], 'a')
        self.assertEqual(self.a.retrieve('" OR *'), [])
        self.a.delete('a')
        self.assertEqual(self.a.retrieve('salmon'), [])

    def test_consent_review_revocation(self):
        with self.assertRaises(ValueError): self.a.stage('a')
        self.a.consent('a', True)
        staged = self.a.stage('a')
        self.assertNotIn('me@example.com', staged['text'])
        self.assertEqual(self.a.approved(), [])
        self.a.review(staged['id'], 'A reviewed learning example')
        self.assertEqual(len(self.a.approved()), 1)
        self.a.consent('a', False)
        self.assertEqual(self.a.approved(), [])

    def test_import_idempotency(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'conversations.json'
            p.write_text(json.dumps([{'id': 'c', 'mapping': {'n': {'message': {
                'author': {'role': 'user'}, 'content': {'parts': ['Hello history']}}}}}]))
            self.assertEqual(self.a.import_export(p), 1)
            self.assertEqual(self.a.import_export(p), 0)
            self.assertEqual(len(self.a.retrieve('Hello')), 1)


if __name__ == '__main__': unittest.main()
