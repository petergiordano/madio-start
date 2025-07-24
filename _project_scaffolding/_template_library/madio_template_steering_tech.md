# Technical Steering Guide

**File:** `tech.md`
**Integration Mode:** `always`
**Purpose:** Provide persistent technical knowledge and constraints to AI agents
**Created:** [DATE]
**Last Modified:** [DATE]

---

## TECHNOLOGY STACK

### **Core AI Platform**
**Primary Platform:** [PLATFORM]
- **Model:** [e.g., Claude Sonnet 4, GPT-4, Gemini Pro]
- **API Endpoints:** [Relevant API information]
- **Rate Limits:** [Request/token limitations]
- **Context Limits:** [Token/character constraints]

**Deployment Platforms:**
- **[Platform 1]:** [e.g., Claude Projects] - [specific configuration notes]
- **[Platform 2]:** [e.g., OpenAI CustomGPT] - [specific considerations]
- **[Platform 3]:** [e.g., Google Gemini Gem] - [platform-specific requirements]

### **Development Stack**
**Languages & Frameworks:**
- **Primary Language:** [e.g., Python, JavaScript, Shell Scripts]
- **Frameworks:** [e.g., FastAPI, Express, Flask]
- **Libraries:** [Key dependencies and versions]

**Infrastructure:**
- **Hosting:** [e.g., AWS, Google Cloud, Azure]
- **Database:** [e.g., PostgreSQL, MongoDB, SQLite]
- **Cache:** [e.g., Redis, Memcached]
- **Message Queue:** [e.g., RabbitMQ, Apache Kafka]

### **MADIO Framework Integration**
**Document Hierarchy:**
- **Tier 1:** `project_system_instructions.md` (Supreme authority)
- **Tier 2:** `orchestrator.md`, `requirements.md`, `design.md`, `tasks.md`
- **Tier 3:** [List of selected supporting documents]

**Template System:**
- **Template Library:** `_project_scaffolding/_template_library/`
- **Template Count:** [Number of available templates]
- **Custom Templates:** [Any project-specific template modifications]

---

## TECHNICAL CONSTRAINTS

### **Performance Requirements**
**Response Time:**
- **Target:** [e.g., < 2 seconds for standard queries]
- **Maximum:** [e.g., < 5 seconds for complex analysis]
- **Timeout:** [e.g., 30 seconds maximum]

**Throughput:**
- **Concurrent Users:** [e.g., Support 100 concurrent sessions]
- **Requests per Second:** [e.g., Handle 50 requests/second]
- **Daily Volume:** [e.g., Process 10,000 requests/day]

**Resource Limits:**
- **Memory:** [e.g., Maximum 2GB RAM usage]
- **Storage:** [e.g., 100GB document storage limit]
- **CPU:** [e.g., 4 core processing capability]

### **Quality Constraints**
**Accuracy Requirements:**
- **Factual Accuracy:** [e.g., >95% for knowledge-based responses]
- **Relevance:** [e.g., >90% relevant to user query]
- **Completeness:** [e.g., Address all aspects of complex queries]

**Safety & Security:**
- **Content Filtering:** [What content must be filtered/blocked]
- **Data Protection:** [PII handling and privacy requirements]
- **Access Control:** [Authentication and authorization requirements]

### **Integration Constraints**
**API Limitations:**
- **Rate Limits:** [Specific API rate limiting details]
- **Data Formats:** [Required input/output formats]
- **Error Handling:** [How to handle API failures]

**Platform Limitations:**
- **Context Length:** [Maximum context per platform]
- **File Upload Limits:** [Document size and type restrictions]
- **Feature Availability:** [Platform-specific feature limitations]

---

## ARCHITECTURAL DECISIONS

### **Design Patterns**
**Architecture Style:** [e.g., Microservices, Monolithic, Serverless]
**Communication Patterns:**
- **Synchronous:** [When to use direct API calls]
- **Asynchronous:** [When to use message queues]
- **Event-Driven:** [Event handling and pub/sub patterns]

**Data Patterns:**
- **Storage Strategy:** [How data is organized and stored]
- **Caching Strategy:** [What and when to cache]
- **Backup Strategy:** [Data backup and recovery approach]

### **Security Architecture**
**Authentication:**
- **Method:** [e.g., OAuth 2.0, API Keys, JWT tokens]
- **Session Management:** [How user sessions are handled]
- **Multi-factor:** [MFA requirements and implementation]

**Authorization:**
- **Role-Based:** [User roles and permissions]
- **Resource-Based:** [Access control for specific resources]
- **Audit Trail:** [Logging and monitoring requirements]

**Data Protection:**
- **Encryption:** [At rest and in transit requirements]
- **Anonymization:** [PII handling and data anonymization]
- **Retention:** [Data retention and deletion policies]

### **Monitoring & Observability**
**Logging:**
- **Log Levels:** [Debug, Info, Warn, Error classification]
- **Log Format:** [Structured logging requirements]
- **Log Retention:** [How long logs are stored]

**Metrics:**
- **Performance Metrics:** [Response time, throughput, error rates]
- **Business Metrics:** [User satisfaction, feature usage]
- **System Metrics:** [CPU, memory, disk usage]

**Alerting:**
- **Critical Alerts:** [System down, high error rates]
- **Warning Alerts:** [Performance degradation, capacity limits]
- **Info Alerts:** [Deployment notifications, scheduled events]

---

## DEVELOPMENT PRACTICES

### **Code Standards**
**Code Style:**
- **Language:** [Language-specific style guide]
- **Formatting:** [Automated formatting tools and rules]
- **Documentation:** [Inline documentation requirements]

**Quality Gates:**
- **Code Review:** [Review process and requirements]
- **Testing:** [Unit, integration, and end-to-end testing]
- **Static Analysis:** [Code analysis tools and thresholds]

### **Version Control**
**Git Workflow:**
- **Branching Strategy:** [e.g., Git Flow, GitHub Flow]
- **Commit Messages:** [Commit message format and conventions]
- **Pull Requests:** [PR template and review process]

**Release Management:**
- **Versioning:** [Semantic versioning or other scheme]
- **Release Process:** [How releases are created and deployed]
- **Rollback Procedures:** [How to rollback problematic releases]

### **Testing Strategy**
**Test Types:**
- **Unit Tests:** [Coverage requirements and frameworks]
- **Integration Tests:** [API and service integration testing]
- **End-to-End Tests:** [User workflow testing]
- **Performance Tests:** [Load and stress testing]

**Test Automation:**
- **CI/CD Pipeline:** [Automated testing in deployment pipeline]
- **Test Environments:** [Development, staging, production testing]
- **Test Data:** [Test data management and privacy]

---

## TECHNICAL DECISION FRAMEWORK

### **Technology Selection Criteria**
**Evaluation Factors:**
1. **Performance:** Does it meet our performance requirements?
2. **Scalability:** Can it grow with our needs?
3. **Reliability:** Is it stable and well-maintained?
4. **Security:** Does it meet our security standards?
5. **Cost:** Is it cost-effective for our budget?
6. **Team Expertise:** Do we have the skills to use it effectively?

### **Technical Debt Management**
**Debt Categories:**
- **High Priority:** [Critical issues affecting performance/security]
- **Medium Priority:** [Issues affecting maintainability]
- **Low Priority:** [Nice-to-have improvements]

**Debt Resolution:**
- **Assessment:** [How to evaluate technical debt impact]
- **Prioritization:** [How to prioritize debt resolution]
- **Planning:** [How to incorporate debt work into sprints]

### **Performance Optimization**
**Optimization Strategy:**
- **Measure First:** [Always measure before optimizing]
- **Profile Bottlenecks:** [Identify actual performance bottlenecks]
- **Optimize Incrementally:** [Make small, measurable improvements]
- **Monitor Impact:** [Verify optimization effectiveness]

---

## INTEGRATION GUIDELINES

### **External APIs**
**API Design Principles:**
- **RESTful Design:** [Follow REST conventions]
- **Versioning:** [API versioning strategy]
- **Documentation:** [API documentation requirements]
- **Error Handling:** [Consistent error response format]

**Third-Party Integrations:**
- **Vendor APIs:** [Guidelines for using external APIs]
- **Rate Limiting:** [How to handle rate limits]
- **Fallback Strategies:** [What to do when external APIs fail]

### **Data Integration**
**Data Sources:**
- **Internal Data:** [Company databases and systems]
- **External Data:** [Third-party data sources]
- **Real-Time Data:** [Streaming data integration]

**Data Quality:**
- **Validation:** [Input data validation requirements]
- **Cleansing:** [Data cleaning and normalization]
- **Monitoring:** [Data quality monitoring and alerting]

---

## AI-SPECIFIC TECHNICAL GUIDANCE

### **Model Integration**
**Context Management:**
- **Context Size:** [How to manage context length limits]
- **Context Relevance:** [How to select relevant context]
- **Context Updates:** [When and how to update context]

**Response Processing:**
- **Output Formatting:** [How to format AI responses]
- **Quality Validation:** [How to validate response quality]
- **Error Recovery:** [How to handle AI errors or poor responses]

### **Prompt Engineering**
**Prompt Design:**
- **Structure:** [How to structure effective prompts]
- **Context Injection:** [How to inject relevant context]
- **Output Specification:** [How to specify desired output format]

**Prompt Management:**
- **Versioning:** [How to version and manage prompts]
- **Testing:** [How to test prompt effectiveness]
- **Optimization:** [How to improve prompt performance]

### **Knowledge Management**
**Document Hierarchy:**
- **Authority:** [How document authority works in MADIO]
- **Dependencies:** [How documents reference each other]
- **Updates:** [How to update interconnected documents]

**Knowledge Updates:**
- **Change Propagation:** [How changes flow through the system]
- **Validation:** [How to validate knowledge consistency]
- **Versioning:** [How to version knowledge updates]

---

## OPERATIONAL GUIDELINES

### **Deployment**
**Deployment Process:**
- **Environments:** [Development → Staging → Production]
- **Validation:** [Pre-deployment validation steps]
- **Rollback:** [Rollback procedures and criteria]

**Configuration Management:**
- **Environment Variables:** [How to manage environment-specific config]
- **Secrets Management:** [How to handle API keys and secrets]
- **Feature Flags:** [How to use feature toggles]

### **Monitoring & Maintenance**
**Health Checks:**
- **System Health:** [What constitutes a healthy system]
- **Performance Monitoring:** [Key performance indicators]
- **Error Monitoring:** [Error tracking and alerting]

**Maintenance Tasks:**
- **Regular Updates:** [Software and dependency updates]
- **Data Maintenance:** [Database cleanup and optimization]
- **Security Updates:** [Security patch management]

---

## TROUBLESHOOTING GUIDE

### **Common Issues**
**Performance Issues:**
- **Slow Responses:** [Diagnostic steps and solutions]
- **High Resource Usage:** [How to identify and resolve]
- **Timeout Errors:** [Common causes and fixes]

**Integration Issues:**
- **API Failures:** [How to diagnose API problems]
- **Authentication Problems:** [Common auth issues]
- **Data Sync Issues:** [Data consistency problems]

### **Diagnostic Tools**
**Monitoring Tools:**
- **Application Monitoring:** [e.g., New Relic, DataDog]
- **Log Analysis:** [e.g., ELK Stack, Splunk]
- **Performance Profiling:** [Language-specific profiling tools]

**Debug Procedures:**
- **Log Analysis:** [How to read and interpret logs]
- **Performance Profiling:** [How to profile performance issues]
- **Error Tracking:** [How to track down error sources]

---

## CHANGE MANAGEMENT

### **Technical Change Process**
**Change Types:**
- **Emergency Changes:** [Critical fixes requiring immediate deployment]
- **Standard Changes:** [Regular feature releases and updates]
- **Major Changes:** [Significant architectural or technology changes]

**Approval Process:**
- **Change Review:** [Who reviews and approves changes]
- **Impact Assessment:** [How to assess change impact]
- **Testing Requirements:** [Testing needed before deployment]

### **Documentation Updates**
**Update Triggers:**
- Technology stack changes
- Architecture modifications
- Performance requirement changes
- Security policy updates
- Integration changes

**Update Process:**
- Document technical changes with rationale
- Update related steering files
- Communicate changes to development team
- Validate AI system behavior with new constraints