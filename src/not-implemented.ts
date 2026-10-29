export function notImplemented(interfaceName: string): never {
  throw new Error(`NOT_IMPLEMENTED: ${interfaceName}`);
}
