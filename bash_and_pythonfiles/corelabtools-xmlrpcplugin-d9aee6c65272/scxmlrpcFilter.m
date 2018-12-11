//
//  cmlrpcFilter.m
//  scxmlrpc
//
//  XML-RPC Generator for MacOS: http://www.ditchnet.org/xmlrpc/
//
//  About XML-RPC: http://www.xmlrpc.com/
//
//  This plugin supports 2 methods for xml-rpc messages
//
//  exportSelectedToPath - {path:"/Users/antoinerosset/Desktop/"}
//
//  openSelectedWithTiling - {rowsTiling:2, columnsTiling:2}
//

#import "scxmlrpcFilter.h"
#import "OsiriXAPI/PluginFilter.h"
#import "OsiriXAPI/DCMPix.h"
#import "OsiriXAPI/ViewerController.h"
#import "OsiriXAPI/DicomFile.h"
#import "OsiriXAPI/BrowserController.h"
#import "OsiriXAPI/DicomDatabase.h"
#import "OsiriXAPI/BrowserController+Sources+Copy.h"
#import "OsiriXAPI/DicomStudy.h"
#import "OsiriXAPI/DicomSeries.h"
#import "OsiriXAPI/DicomImage.h"
#import <Cocoa/Cocoa.h>
//#import "OsiriXAPI/LocalDatabaseNodeIdentifier.h"



@implementation scxmlrpcFilter

+(NSDictionary*)dictionaryForObject:(NSManagedObject*)obj {
    NSMutableDictionary* d = [NSMutableDictionary dictionary];
    
    for (NSString* key in [obj.entity attributesByName]) {
        NSObject* value = [obj valueForKey:key];
        if ([value isKindOfClass:[NSString class]] || [value isKindOfClass:[NSNumber class]] )
            [d setObject:[(NSString*)CFXMLCreateStringByEscapingEntities(NULL, (CFStringRef)value.description, NULL) autorelease] forKey:key];
        if ([value isKindOfClass:[NSDate class]])
        {
            NSTimeZone *tz = [NSTimeZone defaultTimeZone];
            NSInteger seconds = [tz secondsFromGMTForDate: (NSDate*)value];
            NSDate* mydate= [NSDate dateWithTimeInterval: seconds sinceDate: (NSDate*)value];
            [d setObject:[(NSString*)CFXMLCreateStringByEscapingEntities(NULL, (CFStringRef)mydate.description, NULL) autorelease] forKey:key];
        }
        
    }
    
    return d;
}



- (void) initPlugin
{
    NSLog( @"************* xml-rpc plugin init :-)");
    
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(OsiriXXMLRPCMessage:) name:@"OsiriXXMLRPCMessage" object:nil];
}

- (void) OsiriXXMLRPCMessage: (NSNotification*) note
{
    if( [NSThread isMainThread] == NO)
    {
        [self performSelectorOnMainThread:@selector(OsiriXXMLRPCMessage:) withObject: note waitUntilDone: YES];
        return;
    }
    
    @try
    {
        NSMutableDictionary	*httpServerMessage = [note object];
        
        NSLog( @"%@", httpServerMessage);
        
        
        assert([NSThread isMainThread] == YES);
        
        // You will also receive this notification when XMLRPC methods are called through an osirix:// URL
        // In this case, the notification dictionary won't contain an NSXMLDocument and request parameters will be available directly in the dictionary.
        // The following code shows you how to obtain the parameters, no matter if XMLRPC or osirix://
        
        // first, obtain the called method name. its key is "MethodName" from XMLRPC, "methodName" from osirix://
        NSString* methodName = [httpServerMessage objectForKey:@"MethodName"];
        if (!methodName) methodName = [httpServerMessage objectForKey:@"methodName"];
        
        // now that we have the method name, do we want to handle this notification? This plugin provides implementations for 4 methods:
        // updateDICOMNode, importFromURL, exportSelectedToPath and openSelectedWithTiling
        //        if (![methodName isEqualToString: @"updateDICOMNode"] &&
        //            ![methodName isEqualToString: @"importFromURL"] &&
        //            ![methodName isEqualToString: @"exportSelectedToPath"] &&
        //            ![methodName isEqualToString: @"openSelectedWithTiling"])
        //            return; // the cal[\led method is not one of our 4 methods, so just stop handling this notification
        if (![methodName isEqualToString: @"StudyUIDtoSeries"] &&
            ![methodName isEqualToString: @"SeriesUIDtoImages"] &&
            ![methodName isEqualToString: @"SetComment2forSeries"] &&
            ![methodName isEqualToString: @"SetComment3forSeries"] &&
            ![methodName isEqualToString: @"getPatientIDs"] &&
            ![methodName isEqualToString: @"SetComment2forStudy"] &&
            ![methodName isEqualToString: @"SetComment3forSeriesAlessandro"] &&
            ![methodName isEqualToString: @"PatientIDtoStudies"] &&
            ![methodName isEqualToString: @"copySeries2DB"] &&
            ![methodName isEqualToString: @"deleteSeries"])
            
            return; // the cal[\led method is not one of our 4 methods, so just stop handling this notification
        
        
        // since now we're sure we are going to handle this XMLRPC/osirix:// method call, let's build a dictionary with all parameters
        
        // osirix:// calls just put all parameters in the httpServerMessage dictonary, so we first copy it
        NSMutableDictionary* paramDict = [[httpServerMessage mutableCopy] autorelease];
        // XMLRPC calls provide us with a "NSXMLDocument" key containing an NSXMLDocument object
        NSXMLDocument* doc = [httpServerMessage valueForKey:@"NSXMLDocument"];
        if (doc) { // if we have such object, we must extract the parameters from it
            NSString* encoding = [doc characterEncoding];
            NSArray* keys = [doc nodesForXPath:@"methodCall/params//member/name" error:NULL];
            NSArray* values = [doc nodesForXPath:@"methodCall/params//member/value" error:NULL];
            for (int i = 0; i < [keys count]; i++) {
                id value;
                if ([encoding isEqualToString:@"UTF-8"] == NO &&  [[[values objectAtIndex: i] objectValue] isKindOfClass:[NSString class]])
                    value = [(NSString*)CFXMLCreateStringByUnescapingEntities(NULL, (CFStringRef)[[values objectAtIndex: i] objectValue], NULL) autorelease];
                else value = [[values objectAtIndex:i] objectValue];
                [paramDict setValue:value forKey:[[keys objectAtIndex:i] objectValue]];
            }
        }
        
        // now we can use methodName and paramDict
        
        // ****************************************************************************************
        
        if ([methodName isEqualToString: @"SetComment2forStudy"])	//AETitle, Port, TransferSyntax
        {
            //return all studies for this PatientID
            DicomDatabase* idatabase= [DicomDatabase activeLocalDatabase];
            NSError* lerror = nil;
            
            
            //fetch all Series for this for this StudyUID
            //define predicate
            NSString *StudyInstanceUID=[paramDict valueForKey:@"studyInstanceUID"];
            NSString *comment =[paramDict valueForKey:@"Comment"];
            [idatabase lock];
            NSString *request = [NSString stringWithFormat:@"%@%@%@", @"studyInstanceUID='",StudyInstanceUID,@"'"];
            NSPredicate* predicate = [NSPredicate predicateWithFormat:request];
            
            //  NSArray* studies = [idatabase objectsForEntity:@"Study" predicate:predicate error:&lerror];
            
            //this should just be one study
            //  assert([studies count] <=1);
            
            
            
            NSManagedObjectContext *context = idatabase.managedObjectContext;
            
            NSArray* study = [idatabase objectsForEntity:@"Study" predicate:predicate error:&lerror];
            [idatabase unlock];
            assert([study count] ==1);
            NSManagedObjectID* myid=[(DicomStudy*)study[0] objectID];
            
            
            DicomStudy *s = (DicomStudy*) [context objectWithID: myid];
            
            [study[0] willChangeValueForKey: @"comment2"];
            [study[0] setPrimitiveValue: comment forKey: @"comment2"];
            [study[0] didChangeValueForKey: @"comment2"];
            
            // [s setComment:comment];
            [context save:nil];
            //   [idatabase save:NULL];
            
            //   [idatabase save:NULL];
            
            
            
            
            NSString* found_value;
            
            for( id managedObject in study)
            {
                found_value=[managedObject valueForKey:@"comment2"];
                
            }
            
            [httpServerMessage setValue: found_value forKey: @"Response"];
            // [studies[0] setComment:comment];
            [httpServerMessage setValue: [NSNumber numberWithBool: YES] forKey: @"Processed"];
            
        }
        
        if ([methodName isEqualToString: @"SetComment2forSeries"])
        {
            DicomDatabase* idatabase= [DicomDatabase activeLocalDatabase];
            NSError* lerror = nil;
            
            
            //fetch all Series for this for this seriesUID
            //define predicate
            NSString *SeriesInstanceUID=[paramDict valueForKey:@"seriesInstanceUID"];
            NSString *comment =[paramDict valueForKey:@"Comment2"];
            
            NSString *request = [NSString stringWithFormat:@"%@%@%@", @"seriesInstanceUID='",SeriesInstanceUID,@"'"];
            NSPredicate* predicate = [NSPredicate predicateWithFormat:request];
            //       [idatabase release];
            //    [idatabase lock];
            //seems like somehow we need to get this context and save it
            //   studiesArray = [self.database.managedObjectContext executeFetchRequest:dbRequest error:&error];
            //        NSManagedObjectContext *context=idatabase.managedObjectContext;
            // NSManagedObjectContext *context=[idatabase managedObjectContext];
            //    [context retain];
            //     [context lock];
            
            //  [idatabase lock];
            NSManagedObjectContext *context = idatabase.managedObjectContext;
            // [idatabase unlock];
            
            NSArray* series = [idatabase objectsForEntity:@"Series" predicate:predicate error:&lerror];
            assert([series count] ==1);
            NSManagedObjectID* myid=[(DicomSeries*)series[0] objectID];
            
            
            DicomSeries *s = (DicomSeries*) [context objectWithID: myid];
            
            [s willChangeValueForKey: @"comment2"];
            [s setPrimitiveValue: comment forKey: @"comment2"];
            [s didChangeValueForKey: @"comment2"];
            
            
            //[s setComment2:comment];
            
            [context save:nil];
            // [idatabase save:NULL];
            
            
            //  NSArray* series = [idatabase objectsForEntity:@"Series" predicate:predicate error:&lerror];
            
            
            
            
            //this should just be one study
            
            
            
            
            //[series[0] setComment2:comment];
            //for( id managedObject in [self databaseSelection])   //this is from the code run after manual entry
            //what does the id mangeObject mean/do
            // {
            //     [managedObject setValue:object forKey:key];
            // }
            // for( id managedObject in series)
            //  {
            //  @try {
            //      [managedObject setValue:comment forKey:@"comment2"];
            //      NSLog( @"Set comment2 as: %@",comment);
            //  }
            //      @catch (NSException* e)
            //      {
            //         NSLog( @"Exception! %@",e);
            //     }
            //  [managedObject save:NULL];
            
            //   }
            
            
            // [series[0] setValue:comment forKey:@"comment2"];
            //  [[idatabase managedObjectContext] save:NULL];
            //  [idatabase save:NULL];
            
            
            NSString* found_value;
            
            for( id managedObject in series)
            {
                found_value=[managedObject valueForKey:@"comment2"];
                //     NSLog( @"Retrieved comment2 as: %@",found_value);
                
            }
            //NSError* lerror2 = nil;
            //NSString* scS;
            // [idatabase lock];
            //[idatabase unlock];
            //         [context save:nil];
            // [context unlock];
            //   [context release];
            //     BOOL scE=[idatabase save:NULL];
            
            //[refreshTimer setFireDate: [NSDate dateWithTimeIntervalSinceNow:0.5]];
            
            //   NSMutableArray* elements = [NSMutableArray array];
            
            // [elements addObject:[[self class] dictionaryForObject:series[0]]];
            
            [httpServerMessage setValue: found_value forKey: @"Response"];
            // [httpServerMessage setValue: [NSNumber numberWithBool: YES] forKey: @"Processed"];
            [httpServerMessage setValue: [NSNumber numberWithBool: YES] forKey: @"Processed"];
            //  [[[BrowserController currentBrowser] databaseOutline] reloadData];
            //  [[BrowserController currentBrowser.refreshTimer] setFireDate: [NSDate dateWithTimeIntervalSinceNow:0.5];
            //   [idatabase refres
            
            //    NSLog( @"exiting from setcomment2 function db save said: %hhd and thread is %@: ", scE,[NSThread currentThread]);
            
        }
        
        
        if ([methodName isEqualToString: @"SetComment3forSeries"])
        {
            DicomDatabase* idatabase= [DicomDatabase activeLocalDatabase];
            NSError* lerror = nil;
            
            
            //fetch all Series for this for this seriesUID
            //define predicate
            NSString *SeriesInstanceUID=[paramDict valueForKey:@"seriesInstanceUID"];
            NSString *comment =[paramDict valueForKey:@"Comment2"];
            
            NSString *request = [NSString stringWithFormat:@"%@%@%@", @"seriesInstanceUID='",SeriesInstanceUID,@"'"];
            NSPredicate* predicate = [NSPredicate predicateWithFormat:request];
            //       [idatabase release];
            //    [idatabase lock];
            //seems like somehow we need to get this context and save it
            //   studiesArray = [self.database.managedObjectContext executeFetchRequest:dbRequest error:&error];
            //        NSManagedObjectContext *context=idatabase.managedObjectContext;
            // NSManagedObjectContext *context=[idatabase managedObjectContext];
            //    [context retain];
            //     [context lock];
            
            //  [idatabase lock];
            NSManagedObjectContext *context = idatabase.managedObjectContext;
            //   [idatabase unlock];
            
            NSArray* series = [idatabase objectsForEntity:@"Series" predicate:predicate error:&lerror];
            assert([series count] ==1);
            
            
            //probably circular exchange
            NSManagedObjectID* myid=[(DicomSeries*)series[0] objectID];
            DicomSeries *s = (DicomSeries*) [context objectWithID: myid];
            
            //this section works
            //------
            [s willChangeValueForKey: @"comment3"];
            [s setPrimitiveValue: comment forKey: @"comment3"];
            [s didChangeValueForKey: @"comment3"];
            
            [context save:nil];
            //----the below does not in maybe 30% of the calls if the calls are in quick succession
            
            
            // [series[0] setValue:comment forKey:@"comment3"];
            // [[idatabase managedObjectContext] save:NULL];
            //     NSError *error = nil;
            //      BOOL saved = [idatabase save:&error];
            //      if (saved == NO) {
            //          NSLog(@"error = %@", error);
            //       }
            
            
            NSString* found_value;
            
            for( id managedObject in series)
            {
                found_value=[managedObject valueForKey:@"comment3"];
            }
            
            //      if (![found_value isEqualToString: comment])
            //           NSLog(@"error");
            
            [httpServerMessage setValue: found_value forKey: @"Response"];
            [httpServerMessage setValue: [NSNumber numberWithBool: YES] forKey: @"Processed"];
            
        }
        
        
        //        if ([methodName isEqualToString: @"SetComment3forSeriesAlessandro"])
        //        {
        //            DicomDatabase* idatabase= [DicomDatabase activeLocalDatabase];
        //            NSError* lerror = nil;
        //
        //
        //            //fetch all Series for this for this seriesUID
        //            //define predicate
        //            NSString *SeriesInstanceUID=[paramDict valueForKey:@"seriesInstanceUID"];
        //            NSString *comment =[paramDict valueForKey:@"Comment3"];
        //
        //            //NSString *request = [NSString stringWithFormat:@"%@%@%@", @"studyInstanceUID='",StudyInstanceUID,@"'"];
        //            //NSPredicate* predicate = [NSPredicate predicateWithFormat:request];
        //            NSPredicate* predicate = [NSPredicate predicateWithFormat:@"seriesInstanceUID=%@", SeriesInstanceUID];
        //
        //
        //
        //            DicomSeries *s = [[idatabase objectsForEntity:idatabase.seriesEntity predicate:predicate] firstObject];
        //
        //            s.comment3 = comment;
        //
        //
        //            [idatabase save];
        //            //[idatabase lock];
        //            //NSManagedObjectContext *context = idatabase.managedObjectContext;
        //            //[idatabase unlock];
        //
        //            //NSArray* studies = [idatabase objectsForEntity:@"Study" predicate:predicate error:&lerror];
        //            //assert([studies count] ==1);
        //
        //            //[studies[0] setComment3:comment];
        //
        //
        //
        //
        //            //NSManagedObjectID* myid=[(DicomStudy*)studies[0] objectID];
        //
        //
        //            //DicomStudy *s = (DicomStudy*) [context objectWithID: myid];
        //
        //            //[s willChangeValueForKey: @"comment3"];
        //            //[s setPrimitiveValue: comment forKey: @"comment3"];
        //            //[s didChangeValueForKey: @"comment3"];
        //
        //
        //            //[context save:nil];
        //
        //
        //
        //
        //
        //
        //            NSString* found_value;
        //
        //
        //                found_value=[s valueForKey:@"comment3"];
        //
        //
        //            [httpServerMessage setValue: found_value forKey: @"Response"];
        //             [httpServerMessage setValue: [NSNumber numberWithBool: YES] forKey: @"Processed"];
        //
        //        }
        //
        //
        
        if ([methodName isEqualToString: @"deleteSeries"])	//AETitle, Port, TransferSyntax
        {
            //return all studies for this PatientID
            DicomDatabase* idatabase= [DicomDatabase activeLocalDatabase];
            NSError* lerror = nil;
            
            
            //fetch all Series for this for this StudyUID
            //define predicate
            NSString *SeriesInstanceUID=[paramDict valueForKey:@"seriesInstanceUID"];
            NSString *request = [NSString stringWithFormat:@"%@%@%@", @"seriesInstanceUID='",SeriesInstanceUID,@"'"];
            NSPredicate* predicate = [NSPredicate predicateWithFormat:request];
            
            NSArray* series = [idatabase objectsForEntity:@"Series" predicate:predicate error:&lerror];
            
            //this should just be one study
            
            
            
            for (DicomSeries* cseries in series)
                [idatabase.managedObjectContext deleteObject:cseries];
            
            
            [idatabase save];
            
            
            [httpServerMessage setValue: [NSNumber numberWithBool: YES] forKey: @"Processed"];
            
        }
        
        if ([methodName isEqualToString: @"copySeries2DB"])	//AETitle, Port, TransferSyntax
        {
            //return all studies for this PatientID
            NSString *SeriesInstanceUID=[paramDict valueForKey:@"seriesInstanceUID"];
            NSString *targetDB=[paramDict valueForKey:@"targetDB"];
            
            
            DicomDatabase* idatabase= [DicomDatabase activeLocalDatabase];
            NSError* lerror = nil;
            
            
            //fetch all Series for this for this StudyUID
            //define predicate
            NSString *request = [NSString stringWithFormat:@"%@%@%@", @"seriesInstanceUID='",SeriesInstanceUID,@"'"];
            NSPredicate* predicate = [NSPredicate predicateWithFormat:request];
            
            NSArray* series = [idatabase objectsForEntity:@"Series" predicate:predicate error:&lerror];
            
            //this should just be one study
            NSMutableArray* items = [NSMutableArray array];
            for (DicomSeries* cseries in series)
                [items addObject:cseries];
            
            
            //[[idatabase managedObjectContext] deleteObject:cseries];
            
            NSMutableArray* dicomImages = [DicomImage dicomImagesInObjects:items];
            BrowserController* browser=BrowserController.currentBrowser;
            // [DicomDatabase databaseAtPath:<#(NSString *)#> name:<#(NSString *)#>]
    //        DicomDatabase* db=[DicomDatabase existingDatabaseAtPath:targetDB];
            DicomDatabase* db1 = [DicomDatabase databaseAtPath:targetDB name:@"NCCTDWI DB"];
            //[[[BrowserController currentBrowser] sources] arrangedObjects]
          //   NSArray* alldatabases=[DicomDatabase allDatabases];
          //  [DicomDatabase];
            //for (DicomDatabase* db in alldatabases)
            //{
            //    if ([db.name isEqualToString:targetDB])
             //   {
              //      NSLog( @"Found DB name %@", db.name);
             [browser initiateCopyImages:dicomImages toSource:[db1 dataNodeIdentifier]];
                    
              //      break;
              //  }
                
       //     }
            
            
            
            //OR IMPLEMENT IN-THREAD IF POSSIBLE?
            
            
            //LocalDatabaseNodeIdentifier* targetDBidentifier;
            //[browser initiateCopyImages:dicomImages toSource:targetDBidentifier];
            
            //OR
            //  DicomDatabase *dst = [DicomDatabase databaseAtPath:destination.location]; // Create the mainDatabase on the MAIN thread, if necessary !
            
            //   NSThread* thread = [[[NSThread alloc] initWithTarget:self selector:@selector(copyImagesToLocalBrowserSourceThread:) object:[NSArray arrayWithObjects: [dicomImages valueForKey:@"objectID"], destination, _database, dst, NULL]] autorelease];
            //    thread.name = NSLocalizedString(@"Copying images...", nil);
            //    thread.supportsCancel = YES;
            //
            // [[ThreadsManager defaultManager] addThreadAndStart:thread];
            
            
            //is there a way to wait for this thread here now?
            
            [httpServerMessage setValue: @"Bogus" forKey: @"Response"];
            [httpServerMessage setValue: [NSNumber numberWithBool: YES] forKey: @"Processed"];
            
        }
        
        
        
        
        if ([methodName isEqualToString: @"getPatientIDs"])	//AETitle, Port, TransferSyntax
        {
            //return unique patientIDs in database
            DicomDatabase* idatabase= [DicomDatabase activeLocalDatabase];
            NSError* lerror = nil;
            
            
            //fetch all studies and build a set of PatientIDs
            
            NSArray* studies = [idatabase objectsForEntity:@"Study" predicate:nil error:&lerror];
            
            NSMutableSet *set = [[NSMutableSet alloc ]init];
            
            for (DicomStudy *istudy in studies)
            {
                if ([istudy valueForKey:@"patientID"])
                    [set addObject:[istudy valueForKey:@"patientID"]];
                
            }
            
            
            //    NSLog( @"%@", @"test");
            NSArray* myarr= [[set allObjects] mutableCopy];
            
            // Done, we can send the response to the sender
            
            //NSString *xml = @"<?xml version=\"1.0\"?><methodResponse><params><param><value><struct><member><name>error</name><value>0</value></member></struct></value></param></params></methodResponse>";		// Simple answer, no errors
            //NSError *error = nil;
            //NSXMLDocument *doc = [[[NSXMLDocument alloc] initWithXMLString:xml options:NSXMLNodeOptionsNone error:&error] autorelease];
            //[httpServerMessage setValue: doc forKey: @"NSXMLDocumentResponse"];
            [httpServerMessage setValue: myarr forKey: @"Response"];
            [httpServerMessage setValue: [NSNumber numberWithBool: YES] forKey: @"Processed"];		// To tell to other XML-RPC that we processed this order
        }
        
        //TODO: Make test DB of 3 patients and make a duplicate for respawning purposes
        // Implement the functions below
        // Implement making of cases in 2 seperate functions. Was function under DicomDatabase
        
        
        
        
        // ****************************************************************************************
        
        if ([methodName isEqualToString: @"PatientIDtoStudies"])
        {
            //return all studies for this PatientID
            DicomDatabase* idatabase= [DicomDatabase activeLocalDatabase];
            NSError* lerror = nil;
            
            
            //fetch all studies for this ID
            //define predicate
            NSString *patientID=[paramDict valueForKey:@"patientID"];
            NSString *request = [NSString stringWithFormat:@"%@%@%@", @"patientID='",patientID,@"'"];
            NSPredicate* predicate = [NSPredicate predicateWithFormat:request];
            
            NSArray* studies = [idatabase objectsForEntity:@"Study" predicate:predicate error:&lerror];
            
            //put the studyUIDs into an array
            //NSMutableSet *set = [[NSMutableSet alloc ]init];
            
            //            NSMutableArray *StudyInstanceUIDarr = [NSMutableArray new];
            //
            //            for (DicomStudy *istudy in studies)
            //            {
            //
            //                [StudyInstanceUIDarr addObject: [istudy valueForKey:@"StudyInstanceUID"] ];
            //
            //            }
            NSMutableArray* elements = [NSMutableArray array];
            for (DicomStudy *istudy in studies)
            {
                //[ seriesInstanceUID addObject:[s valueForKey:@"SeriesInstanceUID"] ];
                [elements addObject:[[self class] dictionaryForObject:istudy]];
            }
            
            
            
            //    NSLog( @"%@", @"test");
            
            // Done, we can send the response to the sender
            
            //NSString *xml = @"<?xml version=\"1.0\"?><methodResponse><params><param><value><struct><member><name>error</name><value>0</value></member></struct></value></param></params></methodResponse>";		// Simple answer, no errors
            //NSError *error = nil;
            //NSXMLDocument *doc = [[[NSXMLDocument alloc] initWithXMLString:xml options:NSXMLNodeOptionsNone error:&error] autorelease];
            //[httpServerMessage setValue: doc forKey: @"NSXMLDocumentResponse"];
            //[httpServerMessage setValue: StudyInstanceUIDarr forKey: @"Response"];
            [httpServerMessage setValue: elements forKey: @"Response"];
            [httpServerMessage setValue: [NSNumber numberWithBool: YES] forKey: @"Processed"];		// To tell to other XML-RPC that we processed this order
            
            
            
            
        }
        
        // ****************************************************************************************
        
        if ([methodName isEqualToString: @"StudyUIDtoSeries"])
        {
            //return all studies for this PatientID
            DicomDatabase* idatabase= [DicomDatabase activeLocalDatabase];
            NSError* lerror = nil;
            
            
            //fetch all Series for this for this StudyUID
            //define predicate
            NSString *StudyInstanceUID=[paramDict valueForKey:@"studyInstanceUID"];
            NSString *request = [NSString stringWithFormat:@"%@%@%@", @"studyInstanceUID='",StudyInstanceUID,@"'"];
            NSPredicate* predicate = [NSPredicate predicateWithFormat:request];
            
            NSArray* studies = [idatabase objectsForEntity:@"Study" predicate:predicate error:&lerror];
            
            //this should just be one study
            assert([studies count] <=1);
            
            //now get the series of this study object
            NSArray* series = [studies[0] allSeries];
            // NSMutableArray* seriesInstanceUID = [NSMutableArray array];    //need to work out difference between seriedicomuid and series instanceuid. SeriesInstanceUID seems to be a Osirx construct. I assume this is unique in a database sense
            
            
            NSMutableArray* elements = [NSMutableArray array];
            for (DicomSeries* s in series)
            {
                //[ seriesInstanceUID addObject:[s valueForKey:@"SeriesInstanceUID"] ];
                [elements addObject:[[self class] dictionaryForObject:s]];
            }
            
            
            
            
            [httpServerMessage setValue: elements forKey: @"Response"];
            [httpServerMessage setValue: [NSNumber numberWithBool: YES] forKey: @"Processed"];		// To tell to other XML-RPC that we processed this order
            
            
            
            
        }
        
        
        // ****************************************************************************************
        
        if ([methodName isEqualToString: @"SeriesUIDtoImages"])
        {
            //return all studies for this PatientID
            DicomDatabase* idatabase= [DicomDatabase activeLocalDatabase];
            NSError* lerror = nil;
            
            
            //fetch all Series for this for this StudyUID
            //define predicate
            NSString *SeriesInstanceUID=[paramDict valueForKey:@"seriesInstanceUID"];
            NSString *request = [NSString stringWithFormat:@"%@%@%@", @"seriesInstanceUID='",SeriesInstanceUID,@"'"];
            NSPredicate* predicate = [NSPredicate predicateWithFormat:request];
            
            
            
            NSArray* series = [idatabase objectsForEntity:@"Series" predicate:predicate error:&lerror];
            
            
            assert([series count] <=1);
            
            
            //now get the series of this study object
            NSArray* images = [series[0] sortedImages];
            //NSMutableArray* SopInstanceUID = [NSMutableArray array];    //need to work out difference between seriedicomuid and series instanceuid. SeriesInstanceUID seems to be a Osirx construct. I assume this is unique in a database sense
            NSMutableArray* elements = [NSMutableArray array];
            for (DicomImage* i in images)
            {
                //  [ SopInstanceUID addObject:[i valueForKey:@"sopInstanceUID"] ];
                [elements addObject:[[self class] dictionaryForObject:i]];
            }
            
            
            
            
            [httpServerMessage setValue: elements forKey: @"Response"];
            [httpServerMessage setValue: [NSNumber numberWithBool: YES] forKey: @"Processed"];		// To tell to other XML-RPC that we processed this order
            
            
            
            
            
        }
        
        // ****************************************************************************************
        
        NSLog(@"%@", [httpServerMessage description]);
    }
    
    @catch (NSException *e)
    {
        NSLog( @"**** EXCEPTION IN XML-RPC PROCESSING: %@", e);
    }
}

- (long) filterImage : (NSString*) menuName
{
    
    NSRunInformationalAlertPanel( @"XML-RPC Plugin", @"This SC plugin is a XML-RPC message listener.", @"OK", 0L, 0L);
    
    return 0;
}

@end
