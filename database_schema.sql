-- Create the Pathway Table
CREATE TABLE Pathway (
    pathway_id INT AUTO_INCREMENT PRIMARY KEY,      -- Unique identifier for the pathway
    pathway_name VARCHAR(255) NOT NULL,             -- Name of the pathway
    description TEXT,                               -- Description of the pathway
    class TEXT,                                     -- Functional summary of the pathway
    INDEX (pathway_name)                            -- Index for efficient searching by pathway name
);
