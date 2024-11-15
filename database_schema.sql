-- Create the Gene Table
CREATE TABLE Gene (
    gene_id INT AUTO_INCREMENT PRIMARY KEY,         -- Unique identifier for the gene
    gene_name VARCHAR(255) NOT NULL,                -- Name of the gene
    start_position INT NOT NULL,                    -- Start position of the gene
    end_position INT NOT NULL,                      -- End position of the gene
    nucleotide_sequence TEXT NOT NULL,              -- Nucleotide sequence of the gene
    amino_acid_sequence TEXT,                       -- Amino acid sequence, if applicable
    functional_description TEXT,                    -- Functional description of the gene
    pathway_id INT,                                 -- Foreign key reference to the Pathway table
    INDEX (gene_name)                               -- Index for efficient searching by gene name
);

-- Create the Pathway Table
CREATE TABLE Pathway (
    pathway_id INT AUTO_INCREMENT PRIMARY KEY,      -- Unique identifier for the pathway
    pathway_name VARCHAR(255) NOT NULL,             -- Name of the pathway
    pathway_description TEXT,                       -- Description of the pathway
    functional_summary TEXT,                        -- Functional summary of the pathway
    INDEX (pathway_name)                            -- Index for efficient searching by pathway name
);

-- Add foreign key constraint
ALTER TABLE Gene
ADD CONSTRAINT FK_Pathway
FOREIGN KEY (pathway_id) REFERENCES Pathway(pathway_id)
ON DELETE SET NULL;