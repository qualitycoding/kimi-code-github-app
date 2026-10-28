import express from 'express';
import { McpServer } from '@modelcontextprotocol/server';
import { Octokit } from 'octokit';
import { drizzle } from 'drizzle-orm/node-postgres';
import { z } from 'zod';
import pino from 'pino';
import helmet from 'helmet';
import { rateLimit } from 'express-rate-limit';
const app = express(); app.use(helmet()); void [McpServer, Octokit, drizzle, z, pino, rateLimit, app];
