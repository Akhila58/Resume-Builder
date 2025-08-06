import React, { useState } from 'react';
import axios from 'axios';
import { saveAs } from 'file-saver';
import './resumeGenerator.css';

const ResumeGenerator = () => {
  const [jobDescription, setJobDescription] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [pdfUrl, setPdfUrl] = useState(null);
  const [previewMode, setPreviewMode] = useState(false);

  const handleFileChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!jobDescription.trim() || !resumeFile) {
      setError('Please enter a job description and upload your resume');
      return;
    }

    setIsLoading(true);
    setError(null);
    setPdfUrl(null);

    try {
      const formData = new FormData();
      formData.append('job_description', jobDescription);
      formData.append('resume_pdf', resumeFile);

      const response = await axios.post(
        'http://127.0.0.1:8000/generate-resume',
        formData,
        {
          responseType: 'blob',
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = URL.createObjectURL(blob);
      setPdfUrl(url);
    } catch (err) {
      console.error('Error generating resume:', err);
      setError('Failed to generate resume. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    if (pdfUrl) {
      saveAs(pdfUrl, 'generated-resume.pdf');
    }
  };

  return (
    <div className="resume-generator-container">
      <div className="resume-generator">
        <div className="header">
          <h1>AI Resume Generator</h1>
          <p>Enter a job description and upload your resume to get a tailored version</p>
        </div>

        <div className="form-container">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="jobDescription" className="form-label">
                Job Description
              </label>
              <textarea
                id="jobDescription"
                className="textarea"
                placeholder="Paste the job description here..."
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label htmlFor="resumeUpload" className="form-label">
                Upload Your Resume (PDF)
              </label>
              <input
                type="file"
                id="resumeUpload"
                accept=".pdf"
                onChange={handleFileChange}
                className="file-input"
              />
              {resumeFile && (
                <div className="file-info">
                  Selected file: {resumeFile.name}
                </div>
              )}
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
              <button
                type="submit"
                disabled={isLoading}
                className="submit-button"
              >
                {isLoading ? (
                  <>
                    <svg className="spinner" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" width="20" height="20">
                      <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" opacity="0.25"></circle>
                      <path fill="currentColor" opacity="0.75" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Generating...
                  </>
                ) : 'Generate Resume'}
              </button>
            </div>
          </form>

          {error && (
            <div className="error-message">
              <div className="error-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="20" height="20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="error-text">{error}</div>
            </div>
          )}
        </div>

        {pdfUrl && (
          <div className="result-container">
            <div className="result-header">
              <h3 className="result-title">Generated Resume</h3>
              <div className="button-group">
                <button
                  onClick={() => setPreviewMode(!previewMode)}
                  className="secondary-button"
                >
                  {previewMode ? 'Hide Preview' : 'Show Preview'}
                </button>
                <button
                  onClick={handleDownload}
                  className="submit-button"
                >
                  Download PDF
                </button>
              </div>
            </div>

            {previewMode && (
              <div className="pdf-preview">
                <iframe
                  src={pdfUrl}
                  className="pdf-iframe"
                  title="Generated Resume Preview"
                />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ResumeGenerator;