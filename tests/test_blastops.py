import pytest
from blastbesties.blastops import getPairs

# Example BLAST data in format 6
blastAvB_data = """# Query ID\tSubject ID\t% Identity\tAlignment Length\tMismatches\tGap Opens\tQ. Start\tQ. End\tS. Start\tS. End\tE-value\tBit Score
query1\tsubject1\t100.00\t100\t0\t0\t1\t100\t1\t100\t1e-50\t200
query2\tsubject2\t99.00\t100\t1\t0\t1\t100\t1\t100\t1e-40\t180
query3\tsubject3\t98.00\t100\t2\t0\t1\t100\t1\t100\t1e-30\t160
"""

blastBvA_data = """# Query ID\tSubject ID\t% Identity\tAlignment Length\tMismatches\tGap Opens\tQ. Start\tQ. End\tS. Start\tS. End\tE-value\tBit Score
subject1\tquery1\t100.00\t100\t0\t0\t1\t100\t1\t100\t1e-50\t200
subject2\tquery2\t99.00\t100\t1\t0\t1\t100\t1\t100\t1e-40\t180
subject3\tquery3\t98.00\t100\t2\t0\t1\t100\t1\t100\t1e-30\t160
"""

# Additional BLAST data for different test scenarios
blastAvB_data_filtered = """query1\tsubject1\t100.00\t100\t0\t0\t1\t100\t1\t100\t1e-50\t200
query2\tsubject2\t99.00\t100\t1\t0\t1\t100\t1\t100\t1e-40\t180
query3\tsubject3\t98.00\t100\t2\t0\t1\t100\t1\t100\t1e-20\t160
"""

blastBvA_data_filtered = """subject1\tquery1\t100.00\t100\t0\t0\t1\t100\t1\t100\t1e-50\t200
subject2\tquery2\t99.00\t100\t1\t0\t1\t100\t1\t100\t1e-40\t180
subject3\tquery3\t98.00\t100\t2\t0\t1\t100\t1\t100\t1e-20\t160
"""

blastAvB_data_partial = """query1\tsubject1\t100.00\t100\t0\t0\t1\t100\t1\t100\t1e-50\t200
query2\tsubject2\t99.00\t100\t1\t0\t1\t100\t1\t100\t1e-40\t180
"""

blastBvA_data_partial = """subject1\tquery1\t100.00\t100\t0\t0\t1\t100\t1\t100\t1e-50\t200
subject2\tquery2\t99.00\t100\t1\t0\t1\t100\t1\t100\t1e-40\t180
subject3\tquery3\t98.00\t100\t2\t0\t1\t100\t1\t100\t1e-30\t160
"""

@pytest.fixture
def create_blast_files(tmp_path):
    blastAvB = tmp_path / "blastAvB.txt"
    blastBvA = tmp_path / "blastBvA.txt"
    blastAvB.write_text(blastAvB_data)
    blastBvA.write_text(blastBvA_data)
    return blastAvB, blastBvA

@pytest.fixture
def create_filtered_blast_files(tmp_path):
    blastAvB = tmp_path / "blastAvB_filtered.txt"
    blastBvA = tmp_path / "blastBvA_filtered.txt"
    blastAvB.write_text(blastAvB_data_filtered)
    blastBvA.write_text(blastBvA_data_filtered)
    return blastAvB, blastBvA

@pytest.fixture
def create_partial_blast_files(tmp_path):
    blastAvB = tmp_path / "blastAvB_partial.txt"
    blastBvA = tmp_path / "blastBvA_partial.txt"
    blastAvB.write_text(blastAvB_data_partial)
    blastBvA.write_text(blastBvA_data_partial)
    return blastAvB, blastBvA

def test_getPairs(create_blast_files):
    blastAvB, blastBvA = create_blast_files
    result = getPairs(blastAvB, blastBvA)
    expected = [('query1', 'subject1'), ('query2', 'subject2'), ('query3', 'subject3')]
    assert result == expected
    
def test_getPairs_filtered(create_filtered_blast_files):
    blastAvB, blastBvA = create_filtered_blast_files
    result = getPairs(blastAvB, blastBvA, eVal=1e-25)
    expected = [('query1', 'subject1'), ('query2', 'subject2')]
    assert result == expected

def test_getPairs_partial(create_partial_blast_files):
    blastAvB, blastBvA = create_partial_blast_files
    result = getPairs(blastAvB, blastBvA)
    expected = [('query1', 'subject1'), ('query2', 'subject2')]
    assert result == expected

def test_getPairs_minLen(create_blast_files):
    blastAvB, blastBvA = create_blast_files
    result = getPairs(blastAvB, blastBvA, minLen=101)
    expected = []
    assert result == expected

def test_getPairs_bitScore(create_blast_files):
    blastAvB, blastBvA = create_blast_files
    result = getPairs(blastAvB, blastBvA, bitScore=180)
    expected = [('query1', 'subject1'), ('query2', 'subject2')]
    assert result == expected